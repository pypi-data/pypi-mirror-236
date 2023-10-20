import numpy as np
from functools import lru_cache

@lru_cache
def factorial(n):
    """
    Calculate the factorial of a non-negative integer using memoization (caching).

    Parameters:
    n (int): The non-negative integer for which the factorial is computed.

    Returns:
    int: The factorial of n.

    Example:
    >>> factorial(5)
    120
    """
    if n == 0:
        return 1
    return n * factorial(n - 1)

@np.vectorize
def gamma(z):
    """
    Calculate the gamma function for integer values of z.

    Parameters:
    z (numpy.ndarray or int): The input values for which the gamma function is computed.

    Returns:
    numpy.ndarray or float: The gamma function values for the input z.

    Example:
    >>> gamma(5)
    24
    """
    if z == int(z):
        if z > 0:
            return factorial(int(z) - 1)
        elif z == 0:
            return float('inf')
        else:
            raise ValueError("Gamma function is not defined for negative integers.")
    else:
        raise ValueError("Gamma function is not defined for non-integer values of z.")

@np.vectorize
def bessel_function_a_x(a, x, terms=100):
    """
    Compute the Bessel function of the first kind for given values of a and x.

    Parameters:
    a (numpy.ndarray or float): The order of the Bessel function.
    x (numpy.ndarray or float): The argument of the Bessel function.
    terms (int, optional): The number of terms to use in the series expansion (default is 100).

    Returns:
    numpy.ndarray or float: The Bessel function values for the input a and x.

    Example:
    >>> bessel_function_a_x(0, 1)
    0.76519768655797
    """
    result = 0.0
    multiplier = (x / 2) ** a / gamma(a + 1)
    for m in range(terms):
        term = (-1) ** m / (factorial(m) * gamma(m + a + 1)) * (x / 2) ** (2 * m)
        result += term
    return multiplier * result

@np.vectorize
def cos(x):
    """
    Calculate the cosine of an angle in radians using a Taylor series expansion.

    Parameters:
    x (numpy.ndarray or float): The input angle(s) in radians.

    Returns:
    numpy.ndarray or float: The cosine values for the input angle(s).

    Example:
    >>> cos(0)
    1.0
    """
    result = 0
    for n in range(80):
        result += ((-1) ** n) * (x ** (2 * n)) / factorial(2 * n)
    return result

@np.vectorize
def exp(x):
    """
    Calculate the exponential function (e^x) using a Taylor series expansion.

    Parameters:
    x (numpy.ndarray or float): The input value(s) for the exponent.

    Returns:
    numpy.ndarray or float: The exponential function values for the input value(s).

    Example:
    >>> exp(1)
    2.718281828459045
    """
    result = 0.0
    for n in range(80):
        term = (x ** n) / factorial(n)
        result += term
    return result

@np.vectorize
def sin(x):
    """
    Calculate the sine of an angle in radians using a Taylor series expansion.

    Parameters:
    x (numpy.ndarray or float): The input angle(s) in radians.

    Returns:
    numpy.ndarray or float: The sine values for the input angle(s).

    Example:
    >>> sin(0)
    0.0
    """
    result = 0.0
    for n in range(80):
        term = ((-1) ** n) * (x ** (2 * n + 1)) / factorial(2 * n + 1)
        result += term
    return result

@np.vectorize
def tan(x):
    """
    Calculate the tangent of an angle in radians.

    Parameters:
    x (numpy.ndarray or float): The input angle(s) in radians.

    Returns:
    numpy.ndarray or float: The tangent values for the input angle(s).

    Raises:
    ValueError: If the input angle(s) result in a division by zero (cosine is zero).

    Example:
    >>> tan(np.pi / 4)
    0.9999999999999999
    """
    sine = sin(x)
    cosine = cos(x)
    if cosine != 0:
        return sine / cosine
    else:
        raise ValueError("Tangent is undefined for x = pi/2 + k*pi, where k is an integer.")
