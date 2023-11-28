import boto3


class EcrClient:
    def __init__(self):
        self.client = boto3.client('ecr')

    def create_repository(self, name):
        print('Creating ECR repository...')
        self.client.create_repository(repositoryName=name)

    def delete_repository(self, name):
        print('Deleting ECR repository...')
        self.client.delete_repository(repositoryName=name, force=True)

    def get_repository_uri(self, name):
        return self.client.describe_repositories(repositoryNames=[name])['repositories'][0]['repositoryUri']
