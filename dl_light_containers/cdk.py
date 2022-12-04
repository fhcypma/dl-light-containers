#!/usr/bin/env python3

import aws_cdk as cdk
from spark_on_lambda_repo_stack import SparkOnLambdaRepoStack
from dl_light_infra.dataset_app import create_dataset_app
from config import settings


app = cdk.App()

create_dataset_app(
    scope=app,
    name="container-test",
    env=settings.current_env,
    etl_account=settings.aws.accounts.deploy,
    data_account=settings.aws.accounts.deploy,
    ecr_repository_arn=f"arn:aws:ecr:eu-west-1:{settings.aws.accounts.deploy}:repository/spark-on-lambda",
    etl_image_version=settings.image_tag,
    tags=settings.aws.tags,
)

deploy_env = cdk.Environment(account=settings.aws.accounts.deploy, region=settings.aws.region)

SparkOnLambdaRepoStack(
    app,
    etl_accounts=[settings.aws.accounts.etl],
    env=deploy_env,
    tags=settings.aws.tags,
)

app.synth()