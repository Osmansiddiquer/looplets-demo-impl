from src.looplets_py import de_looplets
import pytest
import numpy as np


@pytest.mark.parametrize("value", [-1, 0, 1, 4, -7.21])
def test_runs(value):
    """
    Test the Run expression with different input values.
    """
    # Test with a simple example
    looplet = de_looplets.Pipeline(
        de_looplets.Phase(
            de_looplets.Run(
                de_looplets.Pipeline(
                    de_looplets.Phase(de_looplets.Run(value), stride=2)
                )
            ),
            stride=2,
        )
    )

    for i in range(2):
        for j in range(2):
            assert looplet[i][j] == value


def test_lookup_func():
    """
    Test the Lookup expression with a simple function.
    """

    # Define a simple function for the Lookup expression
    def simple_function(i):
        return i * 2

    # Create a Lookup expression
    looplet = de_looplets.Pipeline(
        de_looplets.Phase(
            de_looplets.Lookup(simple_function),
            stride=2,
        )
    )

    # Test the Lookup expression
    for i in range(2):
        assert looplet[i] == simple_function(i)


def make_lower_triangular(arr):
    """
    Creates a lower triangular matrix from a 1D numpy array.

    Args:
        arr (numpy.ndarray): A 1D numpy array.

    Returns:
         numpy.ndarray: A lower triangular matrix.
    """
    # find the shape of the matrix
    # len of arr = n(n+1)/2
    n = int((np.sqrt(8 * len(arr) + 1) - 1) / 2)
    # create a zero matrix of shape n x n
    mat = np.zeros((n, n))
    # fill the lower triangular part of the matrix
    k = 0
    for i in range(n):
        for j in range(i + 1):
            mat[i][j] = arr[k]
            k += 1
    return mat


def test_lookup_upper_triangular():
    """
    Test the Lookup expression with an array.
    """
    # 15 elements in the array
    v = [
        1.2,
        -2.1,
        3.3,
        -4.4,
        5.5,
        -6.6,
        7.7,
        -8.8,
        3.1,
        -10.1,
        17.54,
        -12.9,
        13.13,
        -14.7,
        15,
    ]

    shape = (5, 5)

    # make a numpy lower triangular matrix
    # with the values in the array
    expected = make_lower_triangular(np.array(v))

    # Create a Lookup expression
    # for row i
    def row(i):
        offset = i * (i + 1) // 2
        print(f"offset: {offset}")
        return de_looplets.Pipeline(
            de_looplets.Phase(
                stride=i+1, body=de_looplets.Lookup(lambda j: v[offset + j])
            ),
            de_looplets.Phase(body=de_looplets.Run(0)),
        )

    arr = de_looplets.Pipeline(
        de_looplets.Phase(
            de_looplets.Lookup(row),
        )
    )

    for i in range(shape[0]):
        for j in range(shape[1]):
            assert (
                arr[i][j] == expected[i][j]
            ), f"Expected {expected[i][j]} but got {arr[i][j]} at ({i}, {j})"
