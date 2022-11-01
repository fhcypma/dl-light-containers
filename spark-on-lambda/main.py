import logging
from typing import Dict, Optional
from datetime import date
from pyspark.sql import SparkSession


logger = logging.getLogger()


def create_spark_session(
    app_name: str, log_level: str = "WARN", config: Optional[Dict[str, str]] = None
) -> SparkSession:
    """Create spark session for local or Lambda use"""
    if not config:
        config = {}

    spark_builder = SparkSession.builder.appName(app_name)
    [spark_builder := spark_builder.config(k, v) for k, v in config.items()]

    logger.info("Starting Spark session")
    spark = spark_builder.getOrCreate()
    spark.sparkContext.setLogLevel(log_level)
    return spark


def execute_job(job_name: str, run_date, spark_config: dict = None):
    spark = create_spark_session(job_name, config=spark_config)
    logger.info("Reading data")
    spark.read.option("header", "true").csv("test_data.csv").show()
    res = {
        "hello": job_name,
        "run_date": str(run_date),
        "config": spark_config,
    }
    return res


# For unit testing the test script (run pip install pyspark)
if __name__ == "__main__":
    execute_job("some-job", date(2022, 1, 1))
