from ray_release.test import (
    Test,
    TestState,
)
from ray_release.test_state.github_client import GithubClient


class TestStateMachine:
    def __init__(self, test: Test) -> None:
        self.test = test
        self.test_results = test.get_test_results(sorted=True)

    def move(self) -> None:
        """
        Move the test state machine forward one step.
        """
        current_state = self.test.get_state()
        state_machine = {
            TestState.JAILED: TestState.PASSING
            if self._jailed_to_passing()
            else (TestState.FAILING if self._jailed_to_failing() else TestState.JAILED),
            TestState.PASSING: TestState.FAILING
            if self._passing_to_failing()
            else (TestState.JAILED if self._passing_to_jailed() else TestState.PASSING),
            TestState.FAILING: TestState.PASSING
            if self._failing_to_passing()
            else (TestState.JAILED if self._failing_to_jailed() else TestState.FAILING),
        }
        next_state = state_machine[self.test.get_state()]
        self.post_move(current_state, next_state)

    def post_move(self, from_state: TestState, to_state: TestState) -> None:
        """
        Post-move hook for the state machine. This is where we do things like
        creating github issues when a test fails.
        """
        if from_state == TestState.JAILED and to_state == TestState.PASSING:
            pass
        elif from_state == TestState.PASSING and to_state == TestState.FAILING:
            self._create_github_issue()
        elif from_state == TestState.FAILING and to_state == TestState.PASSING:
            self._close_github_issue()
        self.test.set_state(to_state)

    def _create_github_issue(self) -> None:
        issue_number = GithubClient().create_release_test_issue(
            self.test, self.test_results[0]
        )
        self.test.set_github_issue_number(issue_number)

    def _close_github_issue(self) -> None:
        # TODO(can): implement this
        pass

    def _jailed_to_passing(self) -> bool:
        # TODO(can): implement this
        return False

    def _jailed_to_failing(self) -> bool:
        # never happen
        return False

    def _passing_to_failing(self) -> bool:
        return (
            len(self.test_results) > 1
            and self.test_results[0].is_failing()
            and self.test_results[1].is_failing()
        )

    def _passing_to_jailed(self) -> bool:
        # never happen
        return False

    def _failing_to_passing(self) -> bool:
        # TODO(can): implement this
        return True

    def _failing_to_jailed(self) -> bool:
        # TODO(can): implement this
        return True
