import pytest
from reflexion.evaluators.programming.local.python import get_func_call

def test_nested():
    assert_statement = 'assert abs(truncate_number(123.456) - 0.456) < 1e-6'
    assert get_func_call(assert_statement) == 'abs(truncate_number(123.456) - 0.456)'

def test_basic_eq():
    assert_statement = 'assert simple_function(arg1, kwarg1=kwarg1) == True'
    assert get_func_call(assert_statement) == 'simple_function(arg1, kwarg1=kwarg1)'

def test_basic_neq():
    assert_statement = 'assert simple_function(arg1, kwarg1=kwarg1) != True'
    assert get_func_call(assert_statement) == 'simple_function(arg1, kwarg1=kwarg1)'

def test_basic_lt():
    assert_statement = 'assert simple_function(arg1, kwarg1=kwarg1) < True'
    assert get_func_call(assert_statement) == 'simple_function(arg1, kwarg1=kwarg1)'

def test_basic_gt():
    assert_statement = 'assert simple_function(arg1, kwarg1=kwarg1) > True'
    assert get_func_call(assert_statement) == 'simple_function(arg1, kwarg1=kwarg1)'

def test_basic_leq():
    assert_statement = 'assert simple_function(arg1, kwarg1=kwarg1) <= True'
    assert get_func_call(assert_statement) == 'simple_function(arg1, kwarg1=kwarg1)'

def test_basic_geq():
    assert_statement = 'assert simple_function(arg1, kwarg1=kwarg1) >= True'
    assert get_func_call(assert_statement) == 'simple_function(arg1, kwarg1=kwarg1)'

def test_basic_negate():
    assert_statement = 'assert not simple_function(arg1, kwarg1=kwarg1)'
    assert get_func_call(assert_statement) == 'simple_function(arg1, kwarg1=kwarg1)'





