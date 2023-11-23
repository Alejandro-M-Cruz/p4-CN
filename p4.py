import subprocess
from time import sleep
from typing import Sequence

import boto3


class CloudFormationClient:
    def __init__(self):
        self.client = boto3.client('cloudformation')

    def create_stack(self, name: str, template: str):
        self.client.create_stack(
            StackName=name,
            TemplateBody=template,
            OnFailure='DELETE'
        )

    def create_stack_from_template_file(self, name: str, file_path: str):
        with open(file_path) as file:
            stack_template = file.read()
        self.create_stack(name, stack_template)

    def delete_stack(self, name: str):
        self.client.delete_stack(StackName=name)

    def stack_exists(self, name: str):
        try:
            self.client.describe_stacks(StackName=name)
            return True
        except self.client.exceptions.ClientError:
            return False


def push_to_erc(project_path: str | None):
    run_bash_command(['./push_to_erc.sh', project_path] if project_path else './push_to_erc.sh')


def run_bash_command(command: str | Sequence[str]):
    try:
        result = subprocess.check_output(
            command,
            shell=True,
            executable='/bin/bash',
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        result = e.output
    for line in result.splitlines():
        print(line.decode())


def main(delete: bool, rebuild: bool):
    cloud_formation_client = CloudFormationClient()
    if delete:
        cloud_formation_client.delete_stack('p4-stack')
        return
    cloud_formation_client.create_stack_from_template_file('p4-stack', file_path='p4_stack.json')
    print('Waiting for stack to be created...')
    while not cloud_formation_client.stack_exists('p4-stack'):
        sleep(1)
    push_to_erc(project_path='server' if rebuild else None)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog='p4.py',
        description='Creates a CloudFormation stack that deploys a node server'
    )
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Whether to delete the stack (default: False)')
    parser.add_argument('-r', '--rebuild', action='store_true',
                        help='Whether to rebuild the Docker image (default: False)')
    args = parser.parse_args()
    main(args.delete, args.rebuild)
