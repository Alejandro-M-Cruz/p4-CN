import subprocess

from cloud_formation_client import CloudFormationClient
from ecr_client import EcrClient

DEFAULT_STACK_NAME = 'p4-fargate-stack'
DEFAULT_STACK_TEMPLATE = 'fargate_ecs_stack.yaml'
ECR_REPOSITORY_NAME = 'p4'
DEFAULT_PROJECT_PATH = 'server'


def push_to_erc(project_path: str):
    print('Pushing to ECR repository...')
    run_bash_command(f"./push_to_erc.sh {ECR_REPOSITORY_NAME} {project_path}")


def run_bash_command(command: str):
    try:
        result = subprocess.check_output(command, shell=True, executable='/bin/bash', stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        result = e.output
    for line in result.splitlines():
        print(line.decode())


def main(**kwargs):
    cloud_formation_client = CloudFormationClient()
    cloud_formation_client.delete_stack(kwargs['name'], wait=True)
    if kwargs['delete']:
        return
    ecr = EcrClient()
    if kwargs['create_repository']:
        ecr.delete_repository(ECR_REPOSITORY_NAME)
        ecr.create_repository(ECR_REPOSITORY_NAME)
        push_to_erc(project_path=kwargs['project_path'])
    cloud_formation_client.create_stack_from_template_file(
        name=kwargs['name'],
        template_path=kwargs['template'],
        template_params={'Image': f'{ecr.get_repository_uri(ECR_REPOSITORY_NAME)}:latest'},
        wait=True
    )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='p4.py',
        description='Creates a CloudFormation stack that deploys a node server via ECS'
    )
    parser.add_argument('-n', '--name', default=DEFAULT_STACK_NAME,
                        help=f'Name of the CloudFormation stack (default: {DEFAULT_STACK_NAME})')
    parser.add_argument('-t', '--template', default=DEFAULT_STACK_TEMPLATE,
                        help=f'Path to the CloudFormation template (default: {DEFAULT_STACK_TEMPLATE})')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Whether to delete the stack and exit (default: False)')
    parser.add_argument('-p', '--project-path', default=DEFAULT_PROJECT_PATH,
                        help=f'Path to the directory containing the Dockerfile (default: {DEFAULT_PROJECT_PATH})')
    parser.add_argument('-r', '--create-repository', action='store_true',
                        help='Whether to create the ECR repository (default: False)')
    args = parser.parse_args()
    main(**args.__dict__)
