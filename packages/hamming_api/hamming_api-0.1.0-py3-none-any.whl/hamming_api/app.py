import os
import pathlib

import fire
import pyspark.sql as sql
import werkzeug
from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse

import hamming_api.data as data
import hamming_api.utils as utils

DEFAULT_UPLOAD_FOLDER = str(pathlib.Path(__file__).parent.parent.absolute() / "data")
DEFAULT_MAX_CONTENT_LENGTH = 1 * 1000 * 1000
DEFAULT_DATABASE_PATH = DEFAULT_UPLOAD_FOLDER + "/database.parquet"
DEFAULT_CONFIG = "spark.driver.memory=1g,spark.executor.memory=2g"


class App_Class:
    """
    A class to wrap the app and spark session and allow for cli usage.

    Attributes:
        upload_folder (str): The path to the folder where uploaded files should be saved.
        max_content_length (int): The maximum size of a file that can be uploaded.
        database_path (str): The path to the database file.
        master (str): The master for the spark session.
        config (str): The configuration for the spark session.
        app_name (str): The name of the spark app.

    Methods:
        run: Run the app.
    """

    def __init__(
        self,
        upload_folder: str = DEFAULT_UPLOAD_FOLDER,
        max_content_length: int = DEFAULT_MAX_CONTENT_LENGTH,
        database_path: str = DEFAULT_DATABASE_PATH,
        master: str = "local[*]",
        config: str = DEFAULT_CONFIG,
        app_name: str = "hamming-api",
    ) -> None:
        self.upload_folder = pathlib.Path(upload_folder)
        self.max_content_length = max_content_length
        self.database_path = database_path
        self.master = master
        self.config = config
        self.app_name = app_name

    def _create_spark_session(self) -> sql.SparkSession:
        """Create the spark session"""

        # Create the spark session
        config = dict(item.split("=") for item in self.config.split(","))
        spark_session_builder = sql.SparkSession.builder.appName(self.app_name).master(self.master)
        for key, value in config.items():
            spark_session_builder = spark_session_builder.config(key, value)

        return spark_session_builder.getOrCreate()

    def _create_flask_app(self) -> Flask:
        """Create the Flask app"""

        # Create the Flask app
        app = Flask(__name__)
        app.config["UPLOAD_FOLDER"] = str(self.upload_folder)
        app.config["MAX_CONTENT_LENGTH"] = self.max_content_length
        api = Api(app)
        parser = reqparse.RequestParser()
        parser.add_argument("sequence")
        api.add_resource(
            HammingMatches,
            "/hamming-matches",
            resource_class_kwargs={
                "database_path": self.database_path,
                "spark_session": self.spark_session,
                "parser": parser,
            },
        )

        @app.route("/")
        def app_upload() -> str:
            return render_template("upload.html")

        @app.route("/upload-result", methods=["POST"])
        def app_upload_result() -> str:
            """Upload a file to the server"""
            if request.method == "POST":
                uploaded_file = request.files["file"]
                if uploaded_file:
                    # Check if the filename ends with .fasta.gz
                    if not uploaded_file.filename.endswith(".gz"):
                        return render_template("upload-failure.html", error="File must be a gzipped file")
                    # Save the file to the data folder
                    filename = werkzeug.utils.secure_filename(uploaded_file.filename)
                    uploaded_file.save(os.path.join(self.upload_folder, filename))
                    # Convert the file to Parquet
                    utils.fastagz_to_parquet(
                        input_path=str(self.upload_folder / uploaded_file.filename),
                        output_path=str(self.database_path) + ".tmp",
                    )
                    # Clean the sequences
                    sequences = self.spark_session.read.parquet(str(self.database_path) + ".tmp")
                    # Parallelize spark dataframe
                    sequences = sequences.repartition(100)
                    sequences = data.clean_sequences(sequences)
                    sequences = data.explode_fasta_id_column(sequences)
                    sequences.write.parquet(str(self.database_path), mode="overwrite")
                    # Remove the temporary file
                    os.remove(str(self.database_path) + ".tmp")
                    database_df = self.spark_session.read.parquet(str(self.database_path))
                    database_df.createOrReplaceTempView("sequence_db")
                    self.spark_session.sql("CACHE TABLE sequence_db")

                    return render_template("upload-success.html", filename=uploaded_file.filename)
            return render_template("upload-failure.html")

        return app

    def run(
        self,
        debug: bool = False,
        port: int = 8080,
    ) -> None:
        """Run the app"""
        self.spark_session = self._create_spark_session()
        self.app = self._create_flask_app()
        self.app.run(debug=debug, port=port)


class HammingMatches(Resource):  # type: ignore[no-any-unimported]
    def __init__(  # type: ignore[no-any-unimported]
        self,
        database_path: str,
        spark_session: sql.SparkSession,
        parser: reqparse.RequestParser,
    ) -> None:
        super().__init__()
        self.database_path = database_path
        self.spark_session = spark_session
        self.parser = parser

    def post(self) -> tuple[dict, int]:
        """Get sequences at a levenshtein distance of 1"""

        # Get the sequence from the request
        args = self.parser.parse_args()
        sequence = args["sequence"]

        # Check to make sure the database has been uploaded
        if not os.path.exists(self.database_path):
            return {"error": "Database not found"}, 404
        # Check if the database is in the spark session
        if not self.spark_session.catalog._jcatalog.tableExists("sequence_db"):
            database_df = self.spark_session.read.parquet(str(self.database_path))
            database_df.createOrReplaceTempView("sequence_db")
            self.spark_session.sql("CACHE TABLE sequence_db")

        # Get the matches
        matches = data.get_hamming_matches(
            spark_session=self.spark_session, view="sequence_db", sequence=sequence, distance=1
        )

        return {"matches": matches}, 200


def main() -> None:
    """Run the app"""
    fire.Fire(App_Class)


if __name__ == "__main__":
    main()
