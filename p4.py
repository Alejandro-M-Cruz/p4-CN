import subprocess
from pprint import pprint
from typing import Sequence

import boto3


def create_cloud_formation_stack(stack_name: str, stack_template: str):
    client = boto3.client('cloudformation')
    client.create_stack(
        StackName=stack_name,
        TemplateBody=stack_template,
        OnFailure='DELETE'
    )


def push_to_erc(project_path: str):
    run_bash_command(['./push_to_erc.sh', project_path])


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
    pprint(result.decode())


if __name__ == '__main__':
    with open('p4_stack.json') as file:
        stack_template = file.read()
    create_cloud_formation_stack('p4-stack', stack_template)
    push_to_erc('server')

