import logging

import typer

from codemodpydanticv1.codemodpydanticv1 import transform_code

cli = typer.Typer()


@cli.command()
def transform(
    file_path: str,
):
    logging.basicConfig(level=logging.INFO)

    with open(file_path) as f:
        code = f.read()

    transformed_code = transform_code(code)

    with open(file_path, "w") as f:
        f.write(transformed_code)
