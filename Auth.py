import boto3
import docker
import base64

ecr_client = boto3.client('ecr', region_name='us-east-1')
docker_client = docker.from_env(timeout=1000)

# Set the ECR repository name and tag
repo_name = 'lambda-function-23'
repo_tag = 'new-image'

# Get the ECR registry URL for the repository
response = ecr_client.describe_repositories(repositoryNames=[repo_name])
registry_url = response['repositories'][0]['registryId'] + \
    '.dkr.ecr.' + 'us-east-1' + '.amazonaws.com'

# Authenticate Docker to the registry
token = ecr_client.get_authorization_token()
username, password = base64.b64decode(
    token['authorizationData'][0]['authorizationToken']).decode().split(':')
registry = token['authorizationData'][0]['proxyEndpoint']
docker_client.login(username, password, registry=registry)

# Build the Docker image
dockerfile_path = '/Users/neethu/Downloads/AWS'
dockerfile = f'{dockerfile_path}/Dockerfile'

image, logs = docker_client.images.build(
    path=dockerfile_path, dockerfile=dockerfile, tag=f'{registry_url}/{repo_name}:{repo_tag}')
for log in logs:
    print(log)

# Push the Docker image to ECR
response = docker_client.images.push(
    f'{registry_url}/{repo_name}:{repo_tag}', stream=True)
for x in response:
    print(x)
