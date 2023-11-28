from time import sleep

import boto3
from botocore.exceptions import ClientError


class EcrClient:
    def __init__(self):
        self.client = boto3.client('ecr')

    def create_repository(self, name):
        self.client.create_repository(repositoryName=name)
        print('Creating ECR repository...')

    def delete_repository(self, name):
        self.client.delete_repository(repositoryName=name, force=True)
        print('Deleting ECR repository...')

    def get_repository_uri(self, name):
        return self.client.describe_repositories(repositoryNames=[name])['repositories'][0]['repositoryUri']
