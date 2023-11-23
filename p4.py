import subprocess

from cloud_formation import CloudFormationClient

STACK_NAME = 'p4-stack'
DEFAULT_STACK_TEMPLATE = 'fargate_ecs_stack.yaml'
ECR_REPOSITORY_NAME = 'p4'


def push_to_erc(project_path: str | None):
    print('Pushing to ERC repository...')
    run_bash_command(f"./push_to_erc.sh {ECR_REPOSITORY_NAME} {project_path or ''}")


def run_bash_command(command: str):
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


def main(**kwargs):
    cloud_formation_client = CloudFormationClient()
    cloud_formation_client.delete_stack(STACK_NAME, wait=True)
    if kwargs['delete']:
        return
    cloud_formation_client.create_stack_from_template_file(STACK_NAME, kwargs['template'], wait=True)
    push_to_erc(project_path=kwargs['project_path'] if kwargs['rebuild'] else None)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='p4.py',
        description='Creates a CloudFormation stack that deploys a node server via ECS'
    )
    parser.add_argument('-t', '--template', default=DEFAULT_STACK_TEMPLATE,
                        help=f'Path to the CloudFormation template (default: {DEFAULT_STACK_TEMPLATE})')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Whether to delete the stack and exit (default: False)')
    parser.add_argument('-p', '--project-path', default='server',
                        help='Path to the directory containing the Dockerfile (default: server)')
    parser.add_argument('-r', '--rebuild', action='store_true',
                        help='Whether to rebuild the container image (default: False)')
    args = parser.parse_args()
    main(**args.__dict__)
