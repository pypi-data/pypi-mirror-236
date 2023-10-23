from __future__ import annotations

import dataclasses
import os
import re
import sys

import libcst as cst
from libcst import matchers as m


def transform_code(code: str) -> str:
    sys.path.append(os.getcwd())

    tree = cst.parse_module(code)
    wrapper = cst.MetadataWrapper(tree)
    tree = wrapper.visit(_PydanticV1Transformer())
    return tree.code


@dataclasses.dataclass(frozen=True)
class _ExactNameReplacementRule:
    _find: str
    _replace: str

    def matches(self, s: str) -> bool:
        return s == self._find

    def replace(self, s: str) -> str:
        return self._replace


@dataclasses.dataclass(frozen=True)
class _RegexNameReplacementRule:
    _find: str
    _replace: str

    def matches(self, s: str) -> bool:
        return re.match(self._find, s) is not None

    def replace(self, s: str) -> str:
        match = re.match(self._find, s)
        assert match is not None
        return self._replace.format(match.group(1))


class _PydanticV1Transformer(m.MatcherDecoratableTransformer):
    METADATA_DEPENDENCIES = (cst.metadata.QualifiedNameProvider,)

    def __init__(self) -> None:
        super().__init__()
        self._exact_replacements: list[_ExactNameReplacementRule] = []
        self._regex_replacements: list[_RegexNameReplacementRule] = []

    @m.call_if_inside(m.Import())
    @m.leave(m.ImportAlias(m.Name("pydantic")))
    def update_pydantic_import(
        self, original_node: cst.ImportAlias, updated_node: cst.ImportAlias
    ) -> cst.ImportAlias:
        self._regex_replacements.append(
            _RegexNameReplacementRule(
                r"^pydantic\.(\w+)$",
                "pydantic_v1.{}",
            )
        )
        return cst.ImportAlias(
            name=_to_attribute("pydantic.v1"),
            asname=cst.AsName(cst.Name("pydantic_v1")),
        )

    @m.call_if_inside(m.Import())
    @m.leave(m.ImportAlias(m.Attribute(m.Name("pydantic"))))
    def update_pydantic_submodule_import(
        self, original_node: cst.ImportAlias, updated_node: cst.ImportAlias
    ) -> cst.ImportAlias:
        submodule_name = original_node.name.attr
        self._regex_replacements.append(
            _RegexNameReplacementRule(
                rf"^pydantic\.{submodule_name.value}\.(\w+)$",
                f"pydantic_v1_{submodule_name.value}.{{}}",
            )
        )
        return cst.ImportAlias(
            name=_to_attribute(f"pydantic.v1.{submodule_name.value}"),
            asname=cst.AsName(cst.Name(f"pydantic_v1_{submodule_name.value}")),
        )

    @m.leave(m.ImportFrom(module=m.Name("pydantic")))
    def update_pydantic_importfrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        import_aliases: list[cst.ImportAlias] = []
        for import_alias in original_node.names:
            self._exact_replacements.append(
                _ExactNameReplacementRule(
                    f"pydantic.{import_alias.name.value}",
                    self._rename_direct_import(import_alias.name.value),
                )
            )
            import_aliases.append(
                cst.ImportAlias(
                    name=import_alias.name,
                    asname=cst.AsName(
                        cst.Name(self._rename_direct_import(import_alias.name.value))
                    ),
                )
            )
        return cst.ImportFrom(
            module=_to_attribute("pydantic.v1"),
            names=import_aliases,
        )

    @m.leave(m.ImportFrom(module=m.Attribute(m.Name("pydantic"))))
    def update_pydantic_submodule_importfrom(
        self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom
    ) -> cst.ImportFrom:
        submodule_name = original_node.module.attr
        import_aliases: list[cst.ImportAlias] = []
        for import_alias in original_node.names:
            self._exact_replacements.append(
                _ExactNameReplacementRule(
                    f"pydantic.{submodule_name.value}.{import_alias.name.value}",
                    self._rename_direct_import(import_alias.name.value),
                )
            )
            import_aliases.append(
                cst.ImportAlias(
                    name=import_alias.name,
                    asname=cst.AsName(
                        cst.Name(self._rename_direct_import(import_alias.name.value))
                    ),
                )
            )
        return cst.ImportFrom(
            module=_to_attribute(f"pydantic.v1.{submodule_name.value}"),
            names=import_aliases,
        )

    def leave_Attribute(
        self, original_node: cst.Attribute, updated_node: cst.Attribute
    ) -> cst.BaseExpression:
        qualified_name = self._get_qualified_name(original_node)
        if (
            not qualified_name
            or qualified_name.source != cst.metadata.QualifiedNameSource.IMPORT
        ):
            return original_node

        for replacement in self._regex_replacements:
            if replacement.matches(qualified_name.name):
                return _to_attribute(replacement.replace(qualified_name.name))

        return original_node

    @m.call_if_not_inside(m.Attribute())
    def leave_Name(
        self, original_node: cst.Name, updated_node: cst.Name
    ) -> cst.BaseExpression:
        qualified_name = self._get_qualified_name(original_node)
        if (
            not qualified_name
            or qualified_name.source != cst.metadata.QualifiedNameSource.IMPORT
        ):
            return original_node

        for replacement in self._exact_replacements:
            if replacement.matches(qualified_name.name):
                return _to_attribute(replacement.replace(qualified_name.name))

        return original_node

    def _get_qualified_name(
        self, node: cst.CSTNode
    ) -> cst.metadata.QualifiedName | None:
        qualified_names = self.get_metadata(cst.metadata.QualifiedNameProvider, node)
        if len(qualified_names) == 0:
            return None
        elif len(qualified_names) > 1:
            raise NotImplementedError
        return qualified_names.pop()

    @staticmethod
    def _rename_direct_import(s: str) -> str:
        return f"PydanticV1{s}" if s[0].isupper() else f"pydantic_v1_{s}"


def _to_attribute(s: str) -> cst.Attribute | cst.Name:
    if "." in s:
        left, right = s.rsplit(".", maxsplit=1)
        return cst.Attribute(value=_to_attribute(left), attr=cst.Name(value=right))
    return cst.Name(value=s)
