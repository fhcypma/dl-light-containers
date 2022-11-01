import datetime
import json
import logging
import os
import zipfile

import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)


LOCAL_ZIP_FILE_NAME = "code.zip"


def download_code(bucket_name: str, key: str):
    logging.info(f"Downloading code s3://{bucket_name}/{key}")

    if os.path.exists(LOCAL_ZIP_FILE_NAME):
        os.remove(LOCAL_ZIP_FILE_NAME)

    s3 = boto3.client("s3", endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))

    try:
        s3.download_file(bucket_name, key, LOCAL_ZIP_FILE_NAME)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logging.error("The object does not exist.")
            raise
        else:
            raise


def unzip_code():
    with zipfile.ZipFile(LOCAL_ZIP_FILE_NAME, "r") as f:
        f.extractall(".")


def execute_code(event, context):
    from main import execute_job

    if "log_level" in event:
        # Using default logging behaviour configured by AWS, setting log level
        log_level = event["log_level"]
        logger.setLevel(logging.getLevelName(log_level))
        logger.info(f"Log level: [{log_level}]")

    assert "job_name" in event, 'No job name provided, set event["job_name"]'
    job_name = event["job_name"]
    logger.info(f"Job name: [{job_name}]")

    assert "run_date" in event, 'No run date provided, set event["run_date"]'
    run_date = datetime.datetime.strptime(event["run_date"], "%Y-%m-%d")
    logger.info(f"Run date: [{run_date}]")

    spark_config = event.get("spark_config", {})
    logger.info(f"Spark config:")
    for k, v in spark_config.items():
        logger.info(f"  {k}: {v}")

    return execute_job(job_name, run_date, spark_config)


def lambda_handler(event, context):
    event = json.loads(event)  # In some way required when running docker locally
    assert "code" in event, 'No key to code provided, set event["code"]'

    code_key = event["code"]
    bucket_name = event["bucket"]
    download_code(bucket_name=bucket_name, key=code_key)
    unzip_code()
    return execute_code(event, context)
