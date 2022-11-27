from typing import List
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_ecr_assets as ecr_assets
from aws_cdk import RemovalPolicy
from cdk_ecr_deployment import DockerImageName, ECRDeployment
from constructs import Construct
from dl_light_infra.stack.types import BasicStack


class SparkOnLambdaRepoStack(BasicStack):
    def __init__(
        self, scope: Construct, etl_accounts: List[str], **kwargs
    ) -> None:
        super().__init__(scope, "ContainerStack", **kwargs)

        # Create repo
        repo = ecr.Repository(
            self,
            "SparkOnLambdaRepo",
            repository_name="spark-on-lambda",
            removal_policy=RemovalPolicy.DESTROY,
            image_scan_on_push=True,
        )
        repo.add_lifecycle_rule(max_image_count=99)
        for account in etl_accounts:
            repo.grant_pull(iam.AccountPrincipal(account))

        # # Publish image to CDK default repo
        # image = ecr_assets.DockerImageAsset(
        #     self,
        #     "SparkOnLambdaImage",
        #     directory="spark-on-lambda",
        # )

        # # Move image from CDK default repo to own repo
        # ECRDeployment(
        #     self,
        #     "SparkOnLambdaImageVersion",
        #     src=DockerImageName(image.image_uri),
        #     dest=DockerImageName(f"{repo.repository_uri}/spark-on-lambda:{image_tag}"),
        # )
