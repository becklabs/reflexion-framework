from typing import List, Sequence

import pandas as pd
from datasets import load_dataset

from .utils import python_extract_tests, rust_extract_tests, string_to_tests


class ProgrammingDataset:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def __getitem__(self, index) -> Sequence:
        """
        Returns a tuple of (question name, signature, docstring, tests)
        """
        row = self.dataset.iloc[index]
        return row["task_id"], row["signature"], row["docstring"], row["test"]

    def __len__(self):
        """
        Returns the number of questions in the dataset
        """
        return len(self.dataset)


class HumanEvalDataset(ProgrammingDataset):
    LANGS = {
        "python": python_extract_tests,
        "rust": rust_extract_tests,
    }

    def __init__(self, language):
        if language not in self.LANGS:
            raise ValueError(f"Language {language} not supported yet.")
        dataset = load_dataset(
            "bigcode/humanevalpack", language, split="test"
        ).to_pandas()
        dataset["test"] = dataset["test"].apply(self.LANGS[language])
        super().__init__(dataset)


class LeetCodeHardDataset(ProgrammingDataset):
    def __init__(self, path: str):
        dataset = pd.read_json(path, lines=True)
        dataset["test"] = dataset["test"].apply(string_to_tests)
        super().__init__(dataset)
