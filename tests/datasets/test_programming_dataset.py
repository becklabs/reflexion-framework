from reflexion.datasets.programming import HumanEvalDataset
from reflexion.datasets.programming import LeetCodeHardDataset
from reflexion.prompts import PROMPTS_DIR
import os

def test_humaneval_python():
    dataset = HumanEvalDataset(language='python')
    qid, signature, docstring, tests = dataset[0]
    assert qid == 'Python/0'
    assert signature ==  'has_close_elements(numbers: List[float], threshold: float) -> bool'
    assert docstring.strip().strip('\n') == """
Check if in given list of numbers, are any two numbers closer to each other than
given threshold.
>>> has_close_elements([1.0, 2.0, 3.0], 0.5)
False
>>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
True
""".strip().strip('\n')
    assert tests ==['assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True', 'assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False', 'assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True', 'assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False', 'assert has_close_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True', 'assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True', 'assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False'] 

def test_humaneval_rust():
    dataset = HumanEvalDataset(language='rust')
    qid, signature, docstring, tests = dataset[0]
    assert qid == 'Rust/0'
    assert signature == 'has_close_elements(numbers:Vec<f32>, threshold: f32) -> bool'
    assert docstring.strip().strip('\n') == """
Check if in given list of numbers, are any two numbers closer to each other than
given threshold. 
""".strip().strip('\n')
    assert tests ==['assert_eq!(has_close_elements(vec![11.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3), true);', 'assert_eq!(has_close_elements(vec![1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05), false);', 'assert_eq!(has_close_elements(vec![1.0, 2.0, 5.9, 4.0, 5.0], 0.95), true);', 'assert_eq!(has_close_elements(vec![1.0, 2.0, 5.9, 4.0, 5.0], 0.8), false);', 'assert_eq!(has_close_elements(vec![1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1), true);', 'assert_eq!(has_close_elements(vec![1.1, 2.2, 3.1, 4.1, 5.1], 1.0), true);', 'assert_eq!(has_close_elements(vec![1.1, 2.2, 3.1, 4.1, 5.1], 0.5), false);'] 

def test_humaneval_rust():
    dataset = LeetCodeHardDataset(path=os.path.join(PROMPTS_DIR, "..", "..", "data", "leetcode-hard-uncontaminated-python3.jsonl"))
    qid, signature, docstring, tests = dataset[0]
    assert qid == "maximize-value-of-function-in-a-ball-passing-game"
    assert signature.strip().strip('\n') == "getMaxFunctionValue(receiver: List[int], k: int) -> int:".strip().strip('\n')
    assert type(docstring) == str

def test_humaneval_rust():
    dataset = LeetCodeHardDataset(path=os.path.join(PROMPTS_DIR, "..", "..", "data", "leetcode-hard-uncontaminated-rust.jsonl"))
    qid, signature, docstring, tests = dataset[0]
    assert qid == "maximize-value-of-function-in-a-ball-passing-game"
    assert type(docstring) == str
    assert signature == "get_max_function_value(receiver: Vec<i32>, k: i64) -> i64"
    assert tests == []

test_humaneval_rust()