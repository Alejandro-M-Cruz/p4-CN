import sys
from datetime import datetime

import boto3


def name_with_datetime(name: str):
    return f"{name}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


def create_cloud_formation_stack(stack_name: str, stack_template: str):
    client = boto3.client('cloudformation')
    client.create_stack(
        StackName=stack_name,
        TemplateBody=stack_template,
        OnFailure='DELETE'
    )




if __name__ == '__main__':
    match len(argv := sys.argv):
        case argc if argc <= 1:
            stack_template_path = 'stack2.json'
            stack_name = name_with_datetime('stack2')
        case argc if argc == 2:
            raise TypeError(
                'Invalid number of arguments. '
                'Usage: python p4.py <stack_template_path> <stack_name>'
            )
        case _:
            stack_template_path = argv[1]
            stack_name = name_with_datetime(argv[2])

    with open(stack_template_path) as file:
        stack_template = file.read()

    create_cloud_formation_stack(stack_name, stack_template)
