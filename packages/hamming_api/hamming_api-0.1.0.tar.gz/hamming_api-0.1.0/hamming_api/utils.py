import gzip
import os

import pandas as pd


def multi_line_fasta_to_single_line(
    input_path: str,
    output_path: str,
) -> None:
    """
    Convert a multi-line FASTA file to a single-line FASTA file.

    Args:
        input_path: Path to the input FASTA file
        output_path: Path to the output FASTA file
        gzip: Whether the input and output files are gzipped
    """

    with gzip.open(input_path, "rt") as input_file, gzip.open(output_path, "wt") as output_file:
        block: list[str] = []
        for line in input_file.readlines():
            if line.startswith(">"):
                if block:
                    output_file.write("".join(block) + "\n")
                    block = []
                output_file.write(line)
            else:
                block.append(line.strip())
        if block:
            output_file.write("".join(block) + "\n")
    return


def single_line_fasta_to_parquet(
    input_path: str,
    output_path: str,
    overwrite: bool = True,
) -> None:
    """
    Convert a single-line FASTA file to a csv file.

    Args:
        input_path: Path to the input FASTA file

    """

    if overwrite and os.path.exists(output_path):
        os.remove(output_path)

    with gzip.open(input_path, "rt") as input_file:
        fasta = input_file.readlines()
        fasta = [x.strip() for x in fasta]
        fasta = [x for x in fasta if x != ""]
        ids = [x for x in fasta if x.startswith(">")]
        ids = [x.replace(">", "") for x in ids]
        sequences = [x for x in fasta if not x.startswith(">")]
        df = pd.DataFrame({"id": ids, "sequence": sequences})
        df.to_parquet(
            output_path,
        )


def fastagz_to_parquet(
    input_path: str,
    output_path: str,
) -> None:
    """
    Convert a gzipped FASTA file to a Parquet file.

    Args:
        input_path: Path to the gzipped FASTA file
        output_path: Path to the output Parquet file
    """

    tmp_fasta_path = input_path.replace(".txt.gz", ".fasta.gz")

    # Convert a multi-line fasta file to a single-line fasta file
    multi_line_fasta_to_single_line(input_path, tmp_fasta_path)

    # Convert the single-line fasta file to a Parquet file
    single_line_fasta_to_parquet(tmp_fasta_path, output_path)

    # Delete the temporary fasta file
    os.remove(tmp_fasta_path)
