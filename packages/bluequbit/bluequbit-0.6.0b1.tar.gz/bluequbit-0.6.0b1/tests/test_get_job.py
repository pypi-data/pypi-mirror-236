import math

import pytest
import qiskit

import bluequbit


# Single precision floating point precision.
# We don't use double precision because Qsim only supports float32 for its
# complex components.
def isclose32(a, b):
    return math.isclose(a, b, rel_tol=1e-6)


def test_get_job():
    dq_client = bluequbit.init()
    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)
    result = dq_client.run(qc_qiskit)

    assert result.num_qubits == 2
    print(result)

    assert result.get_statevector().shape == (4,)
    assert len(result.get_counts()) == 2
    assert isclose32(sum(result.get_counts().values()), 1.0)


def test_get_job2():
    dq_client = bluequbit.init()
    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)
    result = dq_client.run(qc_qiskit)

    result = dq_client.get(result)

    assert result.circuit is not None
    assert result.circuit["circuit_type"] == "Qiskit"
    assert result.num_qubits == 2

    assert result.get_statevector().shape == (4,)
    assert len(result.get_counts()) == 2
    assert isclose32(sum(result.get_counts().values()), 1.0)


def test_get_job_counts():
    dq_client = bluequbit.init()
    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)
    qc_qiskit.measure_all()
    result = dq_client.run(qc_qiskit, shots=6)

    assert result.num_qubits == 2
    assert sum(result.get_counts().values()) == 6
    assert result.shots == 6

    with pytest.raises(bluequbit.exceptions.BQJobStatevectorNotAvailableError) as e:
        result.get_statevector()
    assert (
        e.value.message
        == "Statevector is not available. Job run with shots > 0. Please use"
        " .get_counts() instead."
    )


def test_get_job_counts_nz():
    dq_client = bluequbit.init()
    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)
    qc_qiskit.measure_all()
    result = dq_client.run(qc_qiskit)

    assert result.num_qubits == 2
    assert result.shots is None
    # print(result.get_counts())
    assert sum(result.get_counts().values()) == 1.0


def test_get_job_counts_1000():
    dq_client = bluequbit.init()
    qc_qiskit = qiskit.QuantumCircuit(16)
    for i in range(16):
        if i % 2 == 0:
            qc_qiskit.h(i)
        else:
            qc_qiskit.x(i)
    qc_qiskit.measure_all()
    result = dq_client.run(qc_qiskit, shots=1000)

    assert result.num_qubits == 16
    assert sum(result.get_counts().values()) == 1000
    assert len(result.top_128_results) == 128
    assert result.shots == 1000
    # print(result.get_counts())

    with pytest.raises(bluequbit.exceptions.BQJobStatevectorNotAvailableError) as e:
        result.get_statevector()
    assert (
        e.value.message
        == "Statevector is not available. Job run with shots > 0. Please use"
        " .get_counts() instead."
    )
