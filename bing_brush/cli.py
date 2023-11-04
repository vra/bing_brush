import click

from .bing_brush import BingBrush


@click.command()
@click.option(
    "-c",
    "--cookie",
    help="cookie for https://bing.com, could be a string or a fle path",
)
@click.option("-p", "--prompt", help="prompt")
@click.option(
    "-o",
    "--out_folder",
    default="bing_brush_out_folder",
    help="Location to save generated images",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="if set, enter verbose mode, show detailed logs",
)
def cli(
    cookie,
    prompt,
    out_folder,
    verbose,
):
    """
    image generator using the Bing Image Create API"

    Args:
        cookie (str):
        prompt (str):
        out_folder (str):
        verbose (bool):
    """

    sdk = BingBrush(cookie=cookie, verbose=verbose)

    sdk.process(
        prompt=prompt,
        out_folder=out_folder,
    )
