import boto3
from github import Github
from github.Issue import Issue

from ray_release.test import (
    Test,
    TestResult,
)


class GithubClient:
    github_token = boto3.client(
        "secretsmanager", region_name="us-west-2"
    ).get_secret_value(SecretId="ray_ci_github_token")["SecretString"]["ray-ci-github"]

    def __init__(self):
        self.ray_repo = Github(self.github_token).get_repo("ray-project/ray")

    def create_release_test_issue(self, test: Test, test_result: TestResult) -> Issue:
        return self.ray_repo.create_issue(
            title=f"Release test {test.get_name()} failed",
            body=f"Release test {test.get_name()} failed. "
            "See {test_result.result_url} for more details.",
            labels=["P0", "bug", "release-test"],
            assignee="can-anyscale",
        ).number
