#!/usr/bin/env python3
import aws_cdk as cdk

from container_stack import ContainerStack
from config import settings


target_env = cdk.Environment (
    account=settings.aws.accounts.deploy, region=settings.aws.region
)

app = cdk.App()

ContainerStack(
    app,
    build_number=settings.build_number,
    env=target_env,
    dtap=settings.current_env,
    etl_account=settings.aws.accounts.etl,
    tags=settings.aws.tags,
)

app.synth()
