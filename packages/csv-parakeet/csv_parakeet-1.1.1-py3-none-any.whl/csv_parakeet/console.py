import click
import pandas as pd

from . import __version__


@click.group()
@click.version_option(version=__version__)
def parakeet() -> None:
    """Tool to easily convert between CSV and Parquet files"""
    return None  # pragma: no cover


@parakeet.command()
@click.argument("file_in", type=click.Path(exists=True), nargs=-1)
@click.argument("file_out", type=click.Path(), nargs=1)
def c2p(file_in, file_out):
    """Convert a CSV file to Parquet format

    \b
    Arguments:
        FILE_IN: Path to CSV files. If more than one path is given the CSV files are
        concatenated together.
        FILE_OUT: Desired path for Parquet output
    """
    pd.concat([pd.read_csv(path) for path in file_in], ignore_index=True).to_parquet(
        path=file_out, index=False
    )


@parakeet.command()
@click.argument("file_in", type=click.Path(exists=True), nargs=-1)
@click.argument("file_out", type=click.Path(), nargs=1)
def p2c(file_in, file_out):
    """Convert a Parquet file to CSV format

    \b
    Arguments:
        FILE_IN: Path to Parquet files. If more than one path is given the Parquet
        files are concatenated together.

        FILE_OUT: Desired path for CSV output
    """
    pd.concat([pd.read_parquet(path) for path in file_in], ignore_index=True).to_csv(
        path_or_buf=file_out, index=False
    )
