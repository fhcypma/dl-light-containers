import aws_cdk.aws_iam as iam
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_ecr_assets as ecr_assets
from aws_cdk import RemovalPolicy
from cdk_ecr_deployment import DockerImageName, ECRDeployment
from constructs import Construct
from dl_light_infra.stack.types import BasicStack


class ContainerStack(BasicStack):
    def __init__(
        self, scope: Construct, build_number: str, etl_account: str, **kwargs
    ) -> None:
        super().__init__(scope, "ContainerStack", **kwargs)

        # Create repo
        repo = ecr.Repository(
            self,
            "SparkOnLambdaRepo",
            repository_name=f"spark-on-lambda/base",
            removal_policy=RemovalPolicy.DESTROY,
        )
        repo.add_lifecycle_rule(max_image_count=99)
        repo.grant_pull(iam.AccountPrincipal(etl_account))

        # Publish image to CDK default repo
        image = ecr_assets.DockerImageAsset(
            self,
            "SparkOnLambdaImage",
            directory="spark-on-lambda",
        )

        # Move image from CDK default repo to own repo
        ECRDeployment(
            self,
            "SparkOnLambdaImageVersion",
            src=DockerImageName(image.image_uri),
            dest=DockerImageName(f"{repo.repository_uri}:{build_number}"),
        )
