import cirq
import pytest
from qiskit import QuantumCircuit
from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp

import bluequbit

simulator = cirq.Simulator()


def test_pauli_sum():
    # The circuit and Pauli sums are taken from
    # cirq/sim/sparse_simulator_test.py
    # test_simulate_expectation_values
    q0, q1 = cirq.LineQubit.range(2)
    psum1 = [("ZI", 1), ("IZ", 3.2)]
    psum2 = [("XI", -1), ("IX", 2)]
    c1 = cirq.Circuit(cirq.I(q0), cirq.X(q1))

    def run_compare(circuit, pauli_sum, expected):
        bq = bluequbit.init()
        out = bq.run(circuit, pauli_sum=pauli_sum).expectation_value
        assert cirq.approx_eq(out, expected, atol=1e-6), (out, expected)

    run_compare(c1, psum1, -2.2)
    run_compare(c1, psum2, 0)

    # Test invalid pauli sum
    # More comprehensive test can be found in test_format_pauli_sum of
    # test_tools.py. The goal of this one this is to be an integration test to
    # ensure if an exception happens for an invalid Pauli sum.
    wrong_psum = [None, 1]
    with pytest.raises(Exception) as e:
        bq = bluequbit.init()
        bq.run(c1, pauli_sum=wrong_psum)
    assert f"Unsupported format type for Pauli sum element {None}: {type(None)}" in str(
        e
    )

    # From here on we use our own circuit, not based on Cirq's test cases
    # anymore. We test to ensure the Qiskit, Cirq, and independent run of Cirq
    # all match.
    # Important: the term XII is to test qubit
    # endianness.
    # For Qiskit, XII means the 3rd qubit is X, not the 1st one!
    pauli_sum_expression_qiskit = [
        ("XYZ", 0.5),
        ("XXX", 0.2),
        ("XII", 0.3),
        ("III", 0.4),
    ]
    # Qiskit
    qc_qiskit = QuantumCircuit(3)
    qc_qiskit.h(0)
    qc_qiskit.h(1)
    qc_qiskit.h(2)
    qc_qiskit.ry(0.3, 0)
    qc_qiskit.rz(0.6, 1)
    qc_qiskit.rx(0.7, 2)
    pauli_sum_qiskit = SparsePauliOp.from_list(pauli_sum_expression_qiskit)
    estimator = Estimator()
    expected_qiskit = estimator.run(qc_qiskit, pauli_sum_qiskit).result().values[0]

    # Cirq
    q0, q1, q2 = cirq.LineQubit.range(3)
    c = cirq.Circuit(
        cirq.H(q0),
        cirq.H(q1),
        cirq.H(q2),
        cirq.ry(0.3).on(q0),
        cirq.rz(0.6).on(q1),
        cirq.rx(0.7).on(q2),
    )

    pauli_sum_cirq = (
        0.5 * cirq.X(q2) * cirq.Y(q1) * cirq.Z(q0)
        + 0.2 * cirq.X(q0) * cirq.X(q1) * cirq.X(q2)
        + 0.3 * cirq.X(q2)
        + 0.4 * cirq.I(q0)
    )
    expected_cirq = simulator.simulate_expectation_values(c, pauli_sum_cirq)[0]

    assert cirq.approx_eq(expected_qiskit, expected_cirq, atol=1e-6)
    run_compare(qc_qiskit, pauli_sum_expression_qiskit, expected_qiskit)
    pauli_sum_expression_cirq = [
        (i[0][::-1], i[1]) for i in pauli_sum_expression_qiskit
    ]
    run_compare(c, pauli_sum_expression_cirq, expected_qiskit)

    # This is the 3rd test.
    # The term III is to test that it is not
    # ignored.
    pauli_sum_expression = [("III", 0.4)]
    expected = 0.4
    run_compare(c, pauli_sum_expression, expected)
    run_compare(qc_qiskit, pauli_sum_expression, expected)


def test_list_of_pauli_sum():
    def compare(actual, expected):
        assert len(actual) == len(expected)
        for i in range(len(expected)):
            assert cirq.approx_eq(actual[i], expected[i])

    q0, q1 = cirq.LineQubit.range(2)
    psum1 = [("ZI", 1), ("IZ", 3.2)]
    psum2 = [("XI", -1), ("IX", 2)]
    expected = [-2.2, 0]
    circuit = cirq.Circuit(cirq.I(q0), cirq.X(q1))
    bq = bluequbit.init()
    result = bq.run(circuit, pauli_sum=[psum1, psum2])
    compare(result.expectation_value, expected)

    psum3 = ["ZI + 3.2IZ", "-XI + 2IX"]
    result = bq.run(circuit, pauli_sum=psum3)
    compare(result.expectation_value, expected)

    with pytest.raises(bluequbit.exceptions.BQJobStatevectorNotAvailableError) as e:
        result.get_statevector()
    assert e.value.message == "Statevector is not available. Observables are provided."
