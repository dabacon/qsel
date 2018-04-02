import sys
import time

import numpy as np

S = 'superposition'
E = 'entanglement'


def parse(filename, p0=S, p1=E):
	"""Reads in the give filename and returns all_qubits and the program.

	Args:
		filename: the file to read.
		p0: the token for superposition.
		p1: the token for entanglement.

	Returns:
		A tuple of
			all_qubits: a set of integer indices of all the qubits in the
			program.
			program: A list of dictionaries. Each dictionary contains
			a 'gate' key in {H, CP, M} and the qubits upon which the
			gate operates under the 'qubits' key (as a list).
	Raises:
		SyntaxError: Bad parsing.
	"""
	program = []
	all_qubits = set()
	se = set([p0, p1])
	with open(filename, 'r') as f:
		for line_num, line in enumerate(f):
			tokens = line.strip('\n').split(' ')
			if not all(x in se for x in tokens):
				raise SyntaxError(
					'Only %s and %s allowed error on line %s:\n%s' % 
					(repr(p0), repr(p1), line_num, repr(line)))
			if len(tokens) < 4:
				raise SyntaxError('Not enough tokens:\n%s' % line)
			t0, t1 = tokens[0:2]
			qubits = parse_qubit(tokens[2:], p0, p1)
			all_qubits.update(qubits)
			command = {'qubits': qubits}
			if t0 == p0 and t1 == p0:
				if len(qubits) != 1:
					raise SyntaxError('H gate requires one qubit:\n%s' % line)
				command['gate'] = 'H'
			elif t0 == p1 and t1 == p1:
				if len(qubits) != 2:
					raise SyntaxError('CP gate requires two qubits:\n%s' % line)
				command['gate'] = 'CP'
			else:
				if len(qubits) != 1:
					raise SyntaxError('M gate requires one qubit:\n%s' % line)
				command['gate'] = 'M'
			program.append(command)
	return all_qubits, program


def parse_qubit(tokens, p0, p1):
	if len(tokens) % 2 != 0:
		raise SyntaxError('Invalid number of tokens %d:\n%s' 
			% (len(tokens), ' '.join(tokens)))
	pairs = zip(*[tokens[i::2] for i in range(2)])
	result = ''
	for pair in pairs:
		if pair[0] == p0 and pair[1] == p0:
			result += '0'
		elif pair[0] == p1 and pair[1] == p1:
			result += '1'
		else:
			result += ','
	return [int(x, 2) for x in result.split(',')]


def simulate(qubits, program):
	"""Uses numpy to perform the simulation.

	Args:
		qubits: an iterable of the indices of the qubits.
		program: a list of dictionaries returned from parse.
	"""
	qubit_map = {q : i for q, i in enumerate(list(qubits))}
	n = len(qubits)
	size = 2 ** n
	state = np.zeros(size)
	state[0] = 1.0
	for command in program:
		gate = command['gate']
		qubits = [qubit_map[q] for q in command['qubits']]
		if gate == 'H':
			state = simulate_h(state, qubits, n)
		elif gate == 'CP':
			state = simulate_cp(state, qubits, n)
		else:
			state = simulate_m(state, qubits, n)


def one_project(n, index):
	"""Projector onto the index-th |1><1| for n qubits."""
	return np.tile(np.reshape([np.zeros(2 ** index), np.ones(2 ** index)], - 1),
		2 ** (n - index - 1))


def simulate_h(state, qubits, n):
	index = qubits[0]
	indicized = np.reshape(state, (2 ** (n - index - 1), 2, 2 ** index))
	flip = np.reshape(indicized[:,::-1,:], -1)
	sign = 1 - 2 * one_project(n, index)
	f = 1 / np.sqrt(2)
	state = f * (state * sign + flip)
	return state


def simulate_cp(state, qubits, n):
	index0, index1 = qubits
	state = (1 - (1 - 1j) * one_project(n, index0) * one_project(n, index1)) * state
	return state


def simulate_m(state, qubits, n):
	index = qubits[0]
	one_p = one_project(n, index)
	zero_p = 1 - one_project(n, index)
	state0 = zero_p * state
	prob0 = np.sum(state0 * np.conjugate(state0))
	if np.random.rand() < prob0:
		print('Measured 0 on qubit %d.' % index)
		return state0 / np.sqrt(prob0)
	else:
		print('Measured 1 on qubit %d.' % index)
		state1 = one_p * state
		return state1 / np.sqrt(1 - prob0)

def main():
	np.random.seed(int(time.time()))
	if len(sys.argv) != 2 and len(sys.argv) !=4:
		raise ValueError("Command must be called with a file and "
			"optionally two tokens. "
			"python run.py <file.qsel> <entanglement token> "
			"<superposition token>")
	qubits, program = parse(*sys.argv[1:4])
	simulate(qubits, program)


if __name__ == "__main__":
    main()