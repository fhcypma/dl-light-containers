#!/bin/bash -xe

REGION=eu-west-1
PROFILE=yds-deploy
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --profile "$PROFILE" --query "Account" --output text)
ECR_REPOSITORY_URL="$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
VERSION="20221123.1"
IMAGE_NAME="spark-on-lambda"

# Deploy repo
DYNACONF_BUILD_NUMBER=$VERSION cdk deploy ContainerStack --require-approval never

# Auth
aws ecr get-login-password --region "$REGION" --profile "$PROFILE" | docker login --username AWS --password-stdin "$ECR_REPOSITORY_URL"

# Pulling before building, so we already have certain (or all) layers
docker pull "$IMAGE_NAME:latest" || echo "No latest image available"

# Build new version
docker build -t "$IMAGE_NAME:$VERSION-ci" .

# Upload ci-version
docker tag "$IMAGE_NAME:$VERSION-ci" "$ECR_REPOSITORY_URL/$IMAGE_NAME:$VERSION-ci"
docker push "$ECR_REPOSITORY_URL/$IMAGE_NAME:$VERSION-ci"

# E2E test
DYNACONF_BUILD_NUMBER=$VERSION cdk deploy --all --require-approval never

# Deploy code
zip test.zip main.py
aws s3 cp test.zip s3://yds.tst.container-test.code

# Release
docker tag "$IMAGE_NAME:$VERSION-ci" "$ECR_REPOSITORY_URL/$IMAGE_NAME:$VERSION"
docker push "$ECR_REPOSITORY_URL/$IMAGE_NAME:$VERSION"
docker tag "$IMAGE_NAME:$VERSION-ci" "$ECR_REPOSITORY_URL/$IMAGE_NAME:latest"
docker push "$ECR_REPOSITORY_URL/$IMAGE_NAME:latest"

# Remove build
aws ecr batch-delete-image --repository-name "$IMAGE_NAME" --image-ids imageTag=$VERSION-ci

# Clean up
aws s3 rm s3://yds.tst.container.test.code/test.zip
DYNACONF_BUILD_NUMBER=$VERSION cdk deploy --all --require-approval never