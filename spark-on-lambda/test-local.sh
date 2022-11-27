#!/bin/bash -xe

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"

echo "Starting S3 API"
pip install localstack
pip show localstack
localstack start -d
localstack status
LOCALSTACK_IP=$(docker inspect localstack_main | jq ".[0].NetworkSettings.IPAddress" -r)

echo "Uploading code"
aws s3 mb s3://test --endpoint-url http://localhost:4566
zip test.zip main.py
aws s3 cp test.zip s3://test/ --endpoint-url http://localhost:4566

echo "Building and running spark container"
docker --version
docker build . --tag spark-on-lambda:latest
docker run --rm --detach \
  --publish 9000:8080 \
  --env AWS_ENDPOINT_URL=http://${LOCALSTACK_IP}:4566 \
  --env AWS_ACCESS_KEY_ID=dummy \
  --env AWS_SECRET_ACCESS_KEY=dummy \
  --env AWS_DEFAULT_REGION=eu-west-1 \
  --name spark-on-lambda \
  spark-on-lambda

echo "Waiting 5 seconds for container to initialise"
sleep 5

echo "Triggering Spark job"
# This call usually responds after 48 secodns, but sometimes times out.
RESP=$(curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  --header 'Content-Type: application/json' \
  --data '"{\"job_name\":\"world\",\"log_level\":\"DEBUG\",\"run_date\":\"2022-01-01\",\"bucket\":\"test\",\"code\":\"test.zip\",\"spark_config\":{\"spark.driver.cores\":\"2\",\"spark.sql.shuffle.partitions\":\"1\",\"spark.default.parallelism\":\"1\"}}"' \
  --max-time 90)

echo "Docker logs:"
docker logs spark-on-lambda

echo "Docker response:"
echo "$RESP"

echo "Stopping containers"
docker kill spark-on-lambda
localstack stop

JOB_NAME=$(echo "$RESP" | jq '.hello' -r)
echo $JOB_NAME
RUN_DATE=$(echo "$RESP" | jq '.run_date' -r)
echo $RUN_DATE
CORES=$(echo "$RESP" | jq '.config."spark.driver.cores"' -r)
echo $CORES

if [ "${JOB_NAME}" != "world" ] || [ "${RUN_DATE}" != "2022-01-01 00:00:00" ] || [ "${CORES}" != "2" ]
then
  echo "Spark job did not complete successfully"
  exit 1
fi

echo "Spark job ran successful"
