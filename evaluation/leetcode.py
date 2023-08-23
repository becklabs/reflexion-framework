from typing import Any, List, Sequence

from leetcode_env.environment import LeetCodeEnv
from leetcode_env.types import LeetCodeSubmission, ProgrammingLanguage
from leetcode_env.utils.formatting import (PythonSubmissionFormatter,
                                           RustSubmissionFormatter,
                                           SubmissionFormatter)

from .base import TestingEnv

FORMATTERS = {
    ProgrammingLanguage.PYTHON3: PythonSubmissionFormatter,
    ProgrammingLanguage.RUST: RustSubmissionFormatter,
}


class LeetCodeTestingEnv(TestingEnv):
    def __init__(self, language: ProgrammingLanguage):
        self.formatter: SubmissionFormatter = FORMATTERS.get(language)
        if not self.formatter:
            raise ValueError(f"Unsupported language: {language}")

        self.language = language
        self.leetcode_env = LeetCodeEnv(cooldown=10)

    def step(self, program: str, tests: List[str] = []) -> Sequence:
        submission = LeetCodeSubmission(
            code=self.formatter.to_leetcode(program),
            language=self.language,
            question_slug=None,
            timeout=30,
        )

        status, reward, done, submission_result = self.leetcode_env.step(submission)
