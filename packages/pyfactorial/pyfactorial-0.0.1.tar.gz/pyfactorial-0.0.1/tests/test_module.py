from pyfactorial.module import factorial

def test_factorial_positive_integer():
    result = factorial(5)
    assert result == 120

def test_factorial_zero():
    result = factorial(0)
    assert result == 1

def test_factorial_negative_integer():
    try:
        factorial(-5)
    except ValueError as e:
        assert str(e) == "Factorial is not defined for negative numbers"
