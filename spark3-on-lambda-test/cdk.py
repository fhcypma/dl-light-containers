#!/usr/bin/env python3

import aws_cdk as cdk
from dl_light_infra.dataset_app import create_dataset_app
from config import settings


deploy_env = cdk.Environment(
    account=settings.aws.accounts.deploy, region=settings.aws.region
)

app = cdk.App()

# Just for testing
create_dataset_app(
    scope=app,
    name="container-test",
    env=settings.current_env,
    etl_account=settings.aws.accounts.deploy,
    data_account=settings.aws.accounts.deploy,
    ecr_repository_arn=f"arn:aws:ecr:eu-west-1:{settings.aws.accounts.deploy}:repository/spark3-on-lambda",
    etl_image_version=settings.image_tag,
    tags=settings.aws.tags,
)

app.synth()
