from reflexion.environments.programming import LocalRustTestingEnv

env = LocalRustTestingEnv(timeout=30)

program = """
/*
 Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    
*/
fn has_close_elements(numbers:Vec<f32>, threshold: f32) -> bool{
    for i in 0..numbers.len(){
        for j in 1..numbers.len(){

            if i != j {
                let distance:f32 = numbers[i] - numbers[j];

            if distance < threshold{
                return true;
            }

            }
            
        }
    }

    return false;

}
"""

tests = ['assert_eq!(has_close_elements(vec![11.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3), true);',
'assert_eq!(has_close_elements(vec![1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05), false);',
'assert_eq!(has_close_elements(vec![1.0, 2.0, 5.9, 4.0, 5.0], 0.95), true);',
'assert_eq!(has_close_elements(vec![1.0, 2.0, 5.9, 4.0, 5.0], 0.8), false);',
'assert_eq!(has_close_elements(vec![1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1), true);',
'assert_eq!(has_close_elements(vec![1.1, 2.2, 3.1, 4.1, 5.1], 1.0), true);',
'assert!(has_close_elements(vec![1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == false);']


def test_step():
    reward, messages = env.step(program, tests)
    assert reward == (True, False, True, False, True, True, False)
    assert messages == ('passed', 'failed: execution error: true != false', 'passed', 'failed: execution error: true != false', 'passed', 'passed', 'failed: execution error: assertion failed')

