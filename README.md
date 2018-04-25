## Sequence Partitioning for Process Mining with Unlabeled Event Logs

This repository contains the source code for the paper [Sequence Partitioning for Process Mining with Unlabeled Event Logs](http://web.tecnico.ulisboa.pt/diogo.ferreira/papers/walicki11sequence.pdf) by M. Walicki and D. R. Ferreira in _Data & Knowledge Engineering_ 70(10):821-841, 2011.

### Source files

The original source code used to produce the results described in the paper has been written in Python 2.6 and it comprises the following files:

- `seqpart.py` - This is the file that contains the main algorithms as described in the paper.

- `trie.py` -  This file contains supporting code that is necessary to build and use the trie as described in the paper.

### Running the code

Assuming that Python is installed and available in the system, open a command line and run:
```
$ python seqpart.py abcabababc 2
```
In this example, were are asking for solutions with 2 patterns to the input sequence 'abcabababc'. This will provide the solutions {'abc':2, 'ba':2} and {'abc':2, 'ab':2} (the notation here is that of a Python dictionary).

Note that a pattern is defined as any sequence with non-repeating symbols of length at least 2 and with at least 2 occurrences in the input sequence. If you would like to consider fringes (i.e. single-symbol patterns or patterns with only one occurrence in the sequence) you may run the same program with two additional parameters in order to specify, respectively, the minimum length of each pattern and the minimum number of occurrences of each pattern in the input sequence, as in the following example:
```
$ python seqpart.py abcabababc 2 1 1
```
Here, the last two parameters (which are optional, and have a default value of 2) have been set to 1, which will produce the additional solution {ab:4, c:2} for this sequence.

### How to cite this work

See the [publisher's website](https://www.sciencedirect.com/science/article/pii/S0169023X11000607) to export a citation in the desired format.
