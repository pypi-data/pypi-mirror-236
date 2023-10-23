import pyspark.sql as sql

REFSEQ_KEYS = [
    "gene",
    "locus_tag",
    "db_xref",
    "protein",
    "protein_id",
    "location",
    "gbkey",
]


def parse_fasta_header(
    header: str,
) -> dict[str, str]:
    """
    Parse a FASTA header and return a dictionary containing the header information.

    Args:
        header: FASTA header

    Returns:
        Dictionary containing the header information

    Examples:
        parse_fasta_header("lcl|NC_004828.1_cds_NP_852781.1_2 [gene=Cap 20] [locus_tag=ABC]") == {
            "id": "lcl|NC_004828.1_cds_NP_852781.1_2",
            "gene": "Cap 20",
            "locus_tag": "ABC",
        }
    """

    # Extract the id
    header_list = header.split(" [")

    dictionary: dict[str, str] = {"id": header_list[0]}

    # Extract the key-value pairs
    for item in header_list[1:]:
        try:
            key, value = item.split("=")
        except ValueError:
            raise ValueError(f"Could not parse {header}") from None
        dictionary[key] = value.replace("]", "")

    return dictionary


def clean_sequences(
    sequences: sql.DataFrame,
) -> sql.DataFrame:
    """
    Clean the sequences by applying the following transformations:
    - Remove any non-ACGT characters
    - Convert all characters to uppercase

    Args:
        spark_session: Spark session
        sequences: DataFrame containing the sequences

    Returns:
        DataFrame containing the cleaned sequences
    """

    # Convert all characters to uppercase
    sequences = sequences.withColumn("sequence", sql.functions.upper("sequence"))

    # Remove any non-ACGT characters
    sequences = sequences.withColumn("sequence", sql.functions.regexp_replace("sequence", "[^ACGT]", ""))

    return sequences


def explode_fasta_id_column(
    input_df: sql.DataFrame,
    keys: list[str] = REFSEQ_KEYS,
) -> sql.DataFrame:
    """
    Explode the id column of a DataFrame containing FASTA sequences.

    Args:
        df: DataFrame containing the sequences

    Returns:
        DataFrame containing the sequences with the id column exploded
    """

    # Convert parse_fasta_header to a UDF
    parse_fasta_header_udf = sql.functions.udf(
        parse_fasta_header, sql.types.MapType(sql.types.StringType(), sql.types.StringType())
    )

    # Use the parse_fasta_header function to parse the header
    df = input_df.withColumn("header", parse_fasta_header_udf(sql.functions.col("id"))).withColumn(
        "id", sql.functions.col("header").getItem("id")
    )

    for key in keys:
        df = df.withColumn(key, sql.functions.col("header").getItem(key))
    df = df.drop("header")

    return df


def get_hamming_matches(
    sequence: str,
    spark_session: sql.SparkSession,
    view: str,
    keys: list[str] = REFSEQ_KEYS,
    distance: int = 1,
) -> dict:
    """
    Get sequences from a database at a certain hamming distance from a sequence.

    Args:
        sequence: Sequence to match
        spark_session: Spark session
        view: Name of the view containing the database
        distance: Hamming distance

    Returns:
        A dictionary containing the matches and all of their metadata
    """

    # Get the matches
    matches = spark_session.sql(
        f"""
        SELECT id, sequence, {", ".join(keys)} ,
            LEVENSHTEIN(sequence, "{sequence}") AS distance
        FROM {view}
        WHERE LEVENSHTEIN(sequence, "{sequence}") <= {distance}
        ORDER BY distance
        """
    ).toPandas()

    # Convert the dataframe to a dictionary
    matches.set_index("id", inplace=True)
    matches_dict = matches.to_dict(orient="index")

    return matches_dict
