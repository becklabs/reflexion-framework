from typing import Dict, List, Tuple

from leetcode_env.environment import LeetCodeEnv
from leetcode_env.types import LeetCodeSubmission, ProgrammingLanguage
from leetcode_env.utils.formatting import (
    PythonSubmissionFormatter,
    RustSubmissionFormatter,
    SubmissionFormatter,
)

from .base import TestingEnv

FORMATTERS = {
    ProgrammingLanguage.PYTHON3: PythonSubmissionFormatter,
    ProgrammingLanguage.RUST: RustSubmissionFormatter,
}


class LeetCodeTestingEnv(TestingEnv):
    def __init__(self, language: ProgrammingLanguage, timeout: int = 30):
        self.formatter: SubmissionFormatter = FORMATTERS.get(language)
        if not self.formatter:
            raise ValueError(f"Unsupported language: {language}")

        self.language = language
        self.timeout = timeout
        self.leetcode_env = LeetCodeEnv(cooldown=10)

    def step(
        self, program: str, tests: List[str] = [], metadata: Dict = {}
    ) -> Tuple[List[bool], List[str]]:
        submission = LeetCodeSubmission(
            code=self.formatter.to_leetcode(program),
            language=self.language,
            question_slug=metadata["question_slug"],
            timeout=self.timeout,
        )

        _, reward, _, submission_result = self.leetcode_env.step(submission)

        return reward, submission_result
