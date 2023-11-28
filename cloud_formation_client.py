from time import sleep

import boto3
from botocore.exceptions import ClientError


class CloudFormationClient:
    def __init__(self):
        self.client = boto3.client('cloudformation')

    def create_stack_from_template_file(self, name: str, template_path: str,
                                        *, template_params: dict[str, str], wait=True):
        with open(template_path) as file:
            stack_template = file.read()
        self.create_stack(name, stack_template, template_params=template_params, wait=wait)

    def create_stack(self, name: str, template: str, *, template_params: dict[str, str], wait=True):
        self.client.create_stack(StackName=name, TemplateBody=template, OnFailure='DELETE', Parameters=[
            {'ParameterKey': key, 'ParameterValue': value} for key, value in template_params.items()
        ])
        if wait:
            print('Creating CloudFormation stack...')
            while not self.stack_has_been_created(stack_name=name):
                sleep(3)

    def delete_stack(self, name: str, *, wait=True):
        self.client.delete_stack(StackName=name)
        if wait:
            print('Deleting CloudFormation stack...')
            while not self.stack_has_been_deleted(stack_name=name):
                sleep(3)

    def stack_has_been_created(self, stack_name: str):
        match status := self.get_stack_status(stack_name):
            case 'DELETE_IN_PROGRESS':
                raise RuntimeError('Stack creation failed')
            case _:
                return status == 'CREATE_COMPLETE'

    def stack_has_been_deleted(self, stack_name: str):
        return self.get_stack_status(stack_name) is None

    def get_stack_status(self, stack_name: str):
        try:
            description = self.client.describe_stacks(StackName=stack_name)
            status = description['Stacks'][0]['StackStatus']
            print(f'Current status: {status}')
            return status
        except ClientError:
            return None
