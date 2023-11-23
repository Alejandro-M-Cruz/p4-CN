from time import sleep

import boto3
from botocore.exceptions import ClientError


class CloudFormationClient:
    def __init__(self):
        self.client = boto3.client('cloudformation')

    def create_stack(self, name: str, template: str, *, wait=True):
        self.client.create_stack(
            StackName=name,
            TemplateBody=template,
            OnFailure='DELETE'
        )
        if wait:
            print('Creating CloudFormation stack...')
            while not self.stack_exists('p4-stack'):
                sleep(1)

    def create_stack_from_template_file(self, name: str, template_path: str, *, wait=True):
        with open(template_path) as file:
            stack_template = file.read()
        self.create_stack(name, stack_template, wait=wait)

    def delete_stack(self, name: str, *, wait=True):
        self.client.delete_stack(StackName=name)
        if wait:
            print('Deleting CloudFormation stack...')
            while self.stack_exists('p4-stack'):
                sleep(1)

    def stack_exists(self, name: str):
        try:
            self.client.describe_stacks(StackName=name)
            return True
        except ClientError:
            return False
