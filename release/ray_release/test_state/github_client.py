import boto3
from github import Github

class GithubClient:
    _instance: Github = None

    def __init__(self):
        raise RuntimeError('Initialize a github instead through instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance:
            return cls._instance
        access_token = boto3.client(
            "secretsmanager", region_name="us-west-2"
        ).get_secret_value(SecretId=str(RELEASE_AWS_ANYSCALE_SECRET_ARN))[
            "SecretString"
        ]
        cls._instance = Github(access_token)
        return cls._instance
