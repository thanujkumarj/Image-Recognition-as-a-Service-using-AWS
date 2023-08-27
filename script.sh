#!/bin/bash

# Build the Docker image
docker build -t my-lambda-function .

# Authenticate with the Amazon ECR registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 577149358934.dkr.ecr.us-east-1.amazonaws.com

# Create a repository in Amazon ECR
aws ecr create-repository --repository-name my-lambda-function

# Tag the Docker image with the Amazon ECR repository URL
docker tag my-lambda-function:latest 577149358934.dkr.ecr.us-east-1.amazonaws.com/my-lambda-function:latest

# Push the Docker image to Amazon ECR
docker push 577149358934.dkr.ecr.us-east-1.amazonaws.com/my-lambda-function:latest