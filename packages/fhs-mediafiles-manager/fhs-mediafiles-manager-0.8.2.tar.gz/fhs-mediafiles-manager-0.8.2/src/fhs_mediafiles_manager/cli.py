"""Console script for fhs_mediafiles_manager."""
import sys

import typer
main = typer.Typer()

@main.command()
def help(
        args_default: str = typer.Argument(..., help="Extra help")
):
    """Help."""
    print(
        "Replace this message by putting your code into "
        "fhs_mediafiles_manager.cli.ryb"
    )


@main.command()
def move_media(
        config: str = typer.Argument(..., help="Config file"),
        debug: bool = typer.Option(False, "--debug"),
        dry_run: bool = typer.Option(False, "--dry-run"),

):
    """Move media files.

    Args:
        config: config file
    """
    from .move_media import media_entry
    print(f"{config=} {debug=} {dry_run=}")

    media_entry(config, debug=debug, dry_run=dry_run)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
