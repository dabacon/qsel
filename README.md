# Quantum Super Entangled Language (qsel)

What makes quantum computers more powerful than classical computers?  Ask 
any expert, or watch any public lecture on the subject and the answer
is clear.  **Entanglement** and **Superposition** are what give quantum
computers their power over classical computers.  If these two ideas
are at the heart of the power of quantum computing, it therefore makes
sense that any programing language for quantum computing should make 
these two ideas front and center.  This is where **Quantum Super Entangled
Language** (qsel) comes in.  It is a quantum programming language made
entirely from superposition and entanglement.

## Getting started

The qsel compiler is written in python because who needs strong typing
when you are writing research code that will only ever be seen by yourself
and maybe your graduate students. We recommend you work in a virtual 
environment and pip install the requirements listed in 
[requirements.txt](requirements.txt). Or don't. Yolo.  A sample program 
is provided in [example.qsel](example.qsel). To run this program simply
run the following from your command line
```bash
python run.py example.qsel
```
which should produce something like
```
Measured 1 on qubit 0.
Measured 0 on qubit 1.
```
where your measurement results may be different.

## The Language

Typically quantum computers are described by the abstract quantum circuit
model. In this model the circuits can create entanglement and superposition.
Here we want to use entanglment and superposition to describe a quantum
computation. So our first choice is easy. All of our tokens in the 
language should be either ``entanglement`` or ``superposition``.

A qsel program is specified by a series of lines in a text file.
Each line corresponds to a single ``<command>``. The language is case
sensitive and extremely sensitive to whitespace. This sensitivity is sort
of like a qubit's sensitivity to dephasing.  For dephasing the issue comes
from interacting with uncontrolled degrees of freedom. For qsel the
whitespace sensitivity comes interacting with a lazy programmer.

Back to ``<command>``s. Commands are one of three types
```
<command> -> <entaglement gate> | <superposition gate> | <measurement>
```
Now wait, you say, isn't measurement something beyond entanglement
and superposition?  This is a philosophical and religious question.
Subscribers to it being entanglement belong to the Church of the Higher
Hilbert Space. Those who believe it is superposition find themselves
reading through the many books of the Many Worlds religion.
We don't believe that programming languages should take sides in 
religion or philosophy debates, so we will call it ``<measurement>``,
and you can substitute your personal preference as needed.

### Qubits

Before we describe the three commands, we run into another problem.
If quantum computing is made entirely of entanglement in superposition,
what about the actual objects of a quantum computer, the qubits?
One elegant thought is that maybe we should make the two computational
basis states of our qubit ``entanglement`` and ``superposition``?
Unfortunately this solution appears to cause a recursion which the
universe cannot handle. 
> Religious aside: I think I may have generated some parallel universes
> in which this recursion seg faulted the universe. However if you are
> reading this, then you exist in one of the parallel universe branches
> were I didn't do this.  I guess I'd warn you not to do such 
> experiments, but really I should just make sure you use superposition
> to make sure one of the parallel universes doesn't do the experiment.
> If your religion is not of the Many World's variety, however, your
> view on this may be different and we are very very lucky.

The important thing about qubits is that we need to be able to 
distinguish one qubit from another qubit. Humans have invented
an elegant solution to this problem. They *label* the qubits.
Semi-modern humans found away around the problem of having as 
many labels as objects, by noting that the *label* could be a 
*number*. Modern humans completed this journey by insisting that
the number be written in as a *binary* number so that machines
could understand it. With this insight concerning how to label 
qubits, we define a qubit id made out of one or more binary bits
```
<qubit id> := <bit>+
```
And our bits need to be made out of entanglement and superposition.
```
<bit> := (<superposition> <superposition>) | (<entanglement> <entanglement>)
```
Note that we do not make  the mistake of using a single 
``entanglement`` as the opposite  value of ``superposition``. 
Entanglement can only exist between two objects. From excellent
symmetry considerations, we also double the ``superposition``. 
Finally note some semantics, we interpret the bits as a binary 
string, and compare their values based on this binary value.  So
``<superposition> <superposition> <superposition> superposion>``
is the same as ``<superposition> <superposition>``.

### Commands

We now describe the quantum commands.

The superposition gate starts with a superposition op code (duh),
followed by the id of the gate upon which to act.
```
<superposition gate> := <superposition> <superposition> <qubit id>  
```
What are the semantics of this gate? This corresponds to the 
Hadamard gate.  Because nothing says a modern compiler like using
a gate named after an dead mathematician who wrote down matrices.
This is the gate with matrix
```
[[1/sqrt{2},  1/sqrt{2}],
 [1/sqrt{2}, -1/sqrt{2}]]
```
in the computational basis.

The entanglement gate starts with an entanglment op code (duh),
followed by the ids of the gates upon which to act. Unfortunately
because we need to specify two qubits, we now need some way to
keep these qubits separated from each other.  Otherwise, as we all
know, the qubits interact via an exchange interaction. And it 
is certainly not possible to use exchange interactions only to 
build a quantum computer.  So how do we keep qubits separated?
For this I propose we create an odd kind of monster, a superposition
entanglement divider (since each qubit is one of either type).
Of course this could also be (by symmetry again) an entanglement
superposition divider. So we define
```
<comma> := <entanglement> <superposition> | <superposition> <entanglement>
```
Then we can define the entanglement gate
```
<entanglement gate> := <entanglement> <entanglement> <qubit id> <comma> <qubit id>
```
What are the semantics of this gate? This corresponds to the gate
that I need to make it, along with the Hamadard universal. 
Luckily, Kitaev is a time traveler, and he went to 2027 to 
find out the answer and came back and delivered it to us in 
1997. This is the controlled-P gate, which is the diagonal gate
in the computational basis with diagonal values
```
diag(1, 1, 1, i)
```
There is probably a potty joke here, but one has to have at least
some standards. The good thing is that we don't have to tell you
which qubit is which because controlled-P is symmetric (technically:
bi-urinal).

We next turn to the measurement gate. Measurement,
like we said, is something that, depending on your philosophical
or religious leanings, is either superposition or measurement.
So, following the divider above, we define it as either, followed
by the qubit upon which the measurement is done
```
<measurement> := (<entanglement> <superposition> | <superposition> <entanglement>) <qubit id>
```
Measurement is done in the computational basis.

Finally we need to define ``<superposition>`` and ``<entanglement>``.
But like we said, qsel is all about writing programs in superposition
and entanglement.  So these are the words ``superposition`` and 
``entanglement``, respectively.

One final semantic meaning: we need to define the initial state.
We stick with the boring and state that every qubit used in the 
program starts in the computation 0 state.

## Example

A two qubit circuit. We want to apply Hadamard to the first and
second qubit, then apply the controlled-P gate between the qubits,
finally apply a Hadmard to the second qubit, and measure both
qubits. This is simply
```
superposition superposition superposition superposition
superposition superposition entanglement entanglement
entanglement entanglement superposition superposition entanglement superposition entanglement entanglement
superposition superposition entanglement entanglement
entanglement superposition superposition superposition
entanglement superposition entanglement entanglement
```

## FAQ

**Q:** Wouldn't understanding the difference betwen quantum and classical
polynomial time computing mean proving a major complexity theoretic 
breakthrough like P not equal to PSPACE?

**A:** Yes. Programming languages are regularly places where we present
such proofs. Unlike posting these solutions on the arXiv, putting them
in a programming language insures that only minds who can grok monads
can check the brilliance of the proof.

**Q:** What abou contextuality? Isn't contextuality an important part of
what powers quantum computers?

**A:** Go ahead and ask me that question another time, when you can see
that I am busy or not busy.

**Q:** Isn't entanglement a kind of superposition?

**A:** This is refuted by the fact that such a programming language would
require very inefficient unary encodings.