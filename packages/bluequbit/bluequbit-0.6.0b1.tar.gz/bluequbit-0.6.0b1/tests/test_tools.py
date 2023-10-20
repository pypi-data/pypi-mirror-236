import pytest

from bluequbit import tools


def expect_error_general(func, ps, err_msg):
    with pytest.raises(Exception) as exc_info:
        func(ps)
    assert err_msg in str(exc_info)


def compare(actual, expected):
    assert len(actual) == len(expected)
    for i, e in enumerate(expected):
        ps, coeff = actual[i]
        assert ps == e[0]
        assert coeff == e[1]


def test_parse_pauli_sum_str():
    expected = [("ZI", 2), ("XY", 2), ("XZ", 0.123)]
    compare(tools.parse_pauli_sum_str("2ZI + 2*X*Y + 0.123*XZ"), expected)
    expected = [("Z", -1), ("I", 1)]
    compare(tools.parse_pauli_sum_str("-Z + I"), expected)
    # Whitespace test
    compare(tools.parse_pauli_sum_str("X Y + ZZ"), [("XY", 1), ("ZZ", 1)])
    compare(tools.parse_pauli_sum_str("XXX + 3.2 ZZZ"), [("XXX", 1), ("ZZZ", 3.2)])

    def expect_error(ps, err_msg):
        expect_error_general(tools.parse_pauli_sum_str, ps, err_msg)

    expect_error("2jZI", "Pauli string coefficient must not be complex")
    expect_error(
        "2ZI + 2I",
        "One of the Pauli strings has mismatched length with the first Pauli string",
    )
    expect_error("2xZxI", "Use * for multiplication instead of x")
    expect_error("2Z + + I", "Empty Pauli string element")


def test_format_pauli_sum():
    def expect_error(ps, err_msg):
        expect_error_general(tools.format_pauli_sum, ps, err_msg)

    for obj in [None, 1, 1.2]:
        expect_error(obj, f"Unsupported format type for Pauli sum: {type(obj)}")

    expect_error([], "The Pauli sum is an empty list/tuple")
    wrong = [1, 2], [None, 1]
    for obj in [*wrong, [wrong]]:
        expect_error(
            obj,
            f"Unsupported format type for Pauli sum element {obj[0]}: {type(obj[0])}",
        )

    expected = [("ZZ", 2), ("XX", 3)]
    # Single Pauli sum
    compare(tools.format_pauli_sum(expected), expected)
    # List of Pauli sum
    compare(tools.format_pauli_sum([expected]), [expected])
