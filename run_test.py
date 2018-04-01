import run

import numpy as np
import pytest

F = 1/np.sqrt(2)


def test_one_project():
	np.testing.assert_almost_equal(
		np.array([0, 1]), 
		run.one_project(1, 0))
	np.testing.assert_almost_equal(
			np.array([0, 1, 0, 1]), 
			run.one_project(2, 0))
	np.testing.assert_almost_equal(
		np.array([0, 0, 1, 1]), 
		run.one_project(2, 1))
	np.testing.assert_almost_equal(
		np.array([0, 1, 0, 1, 0, 1, 0, 1]), 
		run.one_project(3, 0))
	np.testing.assert_almost_equal(
		np.array([0, 0, 1, 1, 0, 0, 1, 1]), 
		run.one_project(3, 1))
	np.testing.assert_almost_equal(
		np.array([0, 0, 0, 0, 1, 1, 1, 1]), 
		run.one_project(3, 2))


def matrix(n, update_fn):
	results = []
	for x in range(2 ** n):
		state = np.zeros(2 ** n)
		state[x] = 1.0
		results.append(update_fn(state))
	return np.transpose(np.array(results))


def test_h_one_qubit():
	np.testing.assert_almost_equal(
		np.array([
			[F,  F], 
			[F, -F]]),
		matrix(1, lambda x: run.simulate_h(x, [0], 1)))


def test_h_two_qubits():
	np.testing.assert_almost_equal(
		np.array([
			[F,  F, 0,  0], 
			[F, -F, 0,  0],
			[0,  0, F,  F],
			[0,  0, F, -F]]),
		matrix(2, lambda x: run.simulate_h(x, [0], 2)))
	np.testing.assert_almost_equal(
		np.array([
				[F, 0,  F,  0], 
				[0, F,  0,  F],
				[F, 0, -F,  0],
				[0, F,  0, -F]]),
			matrix(2, lambda x: run.simulate_h(x, [1], 2)))


def test_cp_two_qubits():
	np.testing.assert_almost_equal(
		np.diag([1, 1, 1, 1j]),
		matrix(2, lambda x: run.simulate_cp(x, [0, 1], 2)))


def test_cp_three_qubits():
	np.testing.assert_almost_equal(
		np.diag([1, 1, 1, 1j, 1, 1, 1, 1j]),
		matrix(3, lambda x: run.simulate_cp(x, [0, 1], 3)))
	np.testing.assert_almost_equal(
		np.diag([1, 1, 1, 1j, 1, 1, 1, 1j]),
		matrix(3, lambda x: run.simulate_cp(x, [1, 0], 3)))
	np.testing.assert_almost_equal(
		np.diag([1, 1, 1, 1, 1, 1j, 1, 1j]),
		matrix(3, lambda x: run.simulate_cp(x, [0, 2], 3)))
	np.testing.assert_almost_equal(
		np.diag([1, 1, 1, 1, 1, 1j, 1, 1j]),
		matrix(3, lambda x: run.simulate_cp(x, [2, 0], 3)))
	np.testing.assert_almost_equal(
		np.diag([1, 1, 1, 1, 1, 1, 1j, 1j]),
		matrix(3, lambda x: run.simulate_cp(x, [1, 2], 3)))
	np.testing.assert_almost_equal(
		np.diag([1, 1, 1, 1, 1, 1, 1j, 1j]),
		matrix(3, lambda x: run.simulate_cp(x, [2, 1], 3)))


def measurement_idempotent(n, index):
	for x in range(2 ** n):
		state = np.zeros(2 ** n)
		state[x] = 1.0
		np.testing.assert_almost_equal(state, run.simulate_m(state, [index], n))


def test_measurement_idempotent():
	for n in range(3):
		for index in range(n):
			measurement_idempotent(n, index)


def test_measurement_result_one_qubit(capfd):
	np.random.seed(0)
	state = np.array([F, F])
	state = run.simulate_m(state, [0], 1)
	out, _ = capfd.readouterr()
	assert out.strip() == 'Measured 1 on qubit 0.'
	np.testing.assert_almost_equal(np.array([0, 1]), state)

	np.random.seed(1)
	state = np.array([F, F])
	state = run.simulate_m(state, [0], 1)
	out, _ = capfd.readouterr()
	assert out.strip() == 'Measured 0 on qubit 0.'
	np.testing.assert_almost_equal(np.array([1, 0]), state)

def test_measurement_result_two_qubits(capfd):
 	np.random.seed(0)
 	state = 0.5 * np.array([1, 1, 1, 1])
 	state = run.simulate_m(state, [0], 2)
 	out, _ = capfd.readouterr()
 	assert out.strip() == 'Measured 1 on qubit 0.'
 	np.testing.assert_almost_equal(
 		np.array([0, F, 0, F]), state)


 	np.random.seed(1)
 	state = 0.5 * np.array([1, 1, 1, 1])
 	state = run.simulate_m(state, [0], 2)
 	out, _ = capfd.readouterr()
 	assert out.strip() == 'Measured 0 on qubit 0.'
 	np.testing.assert_almost_equal(
 		np.array([F, 0, F, 0]), state)

 	np.random.seed(0)
 	state = 0.5 * np.array([1, 1, 1, 1])
 	state = run.simulate_m(state, [1], 2)
 	out, _ = capfd.readouterr()
 	assert out.strip() == 'Measured 1 on qubit 1.'
 	np.testing.assert_almost_equal(
 		np.array([0, 0, F, F]), state)

 	np.random.seed(1)
 	state = 0.5 * np.array([1, 1, 1, 1])
 	state = run.simulate_m(state, [1], 2)
 	out, _ = capfd.readouterr()
 	assert out.strip() == 'Measured 0 on qubit 1.'
 	np.testing.assert_almost_equal(
 		np.array([F, F, 0, 0]), state)

def test_parse_qubits():
	assert [0] == run.parse_qubit([run.S, run.S])
	assert [1] == run.parse_qubit([run.E, run.E])
	assert [0] == run.parse_qubit([run.S, run.S, run.S, run.S])
	assert [1] == run.parse_qubit([run.S, run.S, run.E, run.E])
	assert [2] == run.parse_qubit([run.E, run.E, run.S, run.S])
	assert [3] == run.parse_qubit([run.E, run.E, run.E, run.E])
	assert [0, 0] == run.parse_qubit(
		[run.S, run.S, run.S, run.E, run.S, run.S])
	assert [1, 2] == run.parse_qubit(
		[run.E, run.E, run.E, run.S, run.E, run.E, run.S, run.S])


def test_parse_qubits_invalid_token_number():
	with pytest.raises(SyntaxError, matches='number'):
		run.parse_qubit([run.S])
	with pytest.raises(SyntaxError, matches='number'):
		run.parse_qubit([run.S, run.S, run.E])


def test_parse_one_qubit(tmpdir):
	p = tmpdir.join('parse.qsel')
	p.write('superposition superposition superposition superposition\n'
			'superposition entanglement superposition superposition')
	all_qubits, program = run.parse(str(p))
	assert all_qubits == set([0])
	assert program == [
		{'gate': 'H', 'qubits': [0]}, 
		{'gate': 'M', 'qubits': [0]}]


def test_parse_two_qubit(tmpdir):
	p = tmpdir.join('parse.qsel')
	p.write('entanglement entanglement superposition superposition '
				'superposition entanglement entanglement entanglement\n'
			'superposition entanglement superposition superposition')
	all_qubits, program = run.parse(str(p))
	assert all_qubits == set([0, 1])
	assert program == [
		{'gate': 'CP', 'qubits': [0, 1]}, 
		{'gate': 'M', 'qubits': [0]}]


def test_parse_too_few_qubits(tmpdir):
	p = tmpdir.join('parse.qsel')
	p.write('entanglement entanglement superposition')
	with pytest.raises(SyntaxError, match='Not enough'):
		run.parse(str(p))


def test_parse_bad_tokens(tmpdir):
	p = tmpdir.join('parse.qsel')
	p.write('entanglement x')
	with pytest.raises(SyntaxError, match='Only'):
		run.parse(str(p))


def test_parse_h_wrong_qubit_number(tmpdir):
	p = tmpdir.join('parse.qsel')
	p.write(' '.join([run.S, run.S, run.S, run.S, run.S, run.E, run.E, run.E]))
	with pytest.raises(SyntaxError, match='H gate'):
		run.parse(str(p))


def test_parse_cp_wrong_qubit_number(tmpdir):
	p = tmpdir.join('parse.qsel')
	p.write(' '.join([run.E, run.E, run.S, run.S]))
	with pytest.raises(SyntaxError, match='CP gate'):
		run.parse(str(p))


def test_parse_m_wrong_qubit_number(tmpdir):
	p = tmpdir.join('parse.qsel')
	p.write(' '.join([run.S, run.E, run.S, run.S, run.S, run.E, run.E, run.E]))
	with pytest.raises(SyntaxError, match='M gate'):
		run.parse(str(p))

