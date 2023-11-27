from time import sleep

import boto3
from botocore.exceptions import ClientError


class EcrClient:
    def __init__(self):
        self.client = boto3.client('ecr')

    def create_repository(self, name, *, wait=True):
        self.client.create_repository(repositoryName=name)
        if wait:
            print('Creating ECR repository...')
            while not self.repository_exists(name):
                sleep(3)

    def delete_repository(self, name, *, wait=True):
        self.client.delete_repository(repositoryName=name, force=True)
        if wait:
            print('Deleting ECR repository...')
            while self.repository_exists(name):
                sleep(3)

    def repository_exists(self, name):
        try:
            self.client.describe_repositories(repositoryNames=[name])
            return True
        except ClientError:
            return False

    def get_repository_uri(self, name):
        return self.client.describe_repositories(repositoryNames=[name])['repositories'][0]['repositoryUri']
