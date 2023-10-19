import logging
import os.path

import typer

from alvin_cli import dbt
from alvin_cli.config.loader import USER_CONFIG_DIR, create_cfg_file
from alvin_cli.datafakehouse import methods
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)
app.add_typer(dbt.app, name="dbt", help="Dbt related commands")
app.add_typer(methods.app, name="datafakehouse", help="Datafakehouse related commands")


def __setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


@app.command()
def setup(api_key: str = "", overwrite: bool = False) -> None:
    """Set up configuration file and input your alvin credentials"""

    directory = USER_CONFIG_DIR
    if not os.path.isdir(directory):
        os.makedirs(directory)

    is_file_present = create_cfg_file(
        directory_path=directory,
        overwrite=overwrite,
        api_key=api_key or None,
    )

    if is_file_present:
        typer_secho_raise(
            f"File in {directory}/alvin.cfg already exists. Fill your credentials to start using other commands!",
            "CYAN",
        )
        return

    typer_secho_raise(
        f"Created file 'alvin.cfg'. Set up your credentials in {directory}/alvin.cfg"
        f" to start using other commands!",
        "GREEN",
    )


def run() -> None:
    app()


# deploy 01
if __name__ == "__main__":
    run()  # pragma: no cover
