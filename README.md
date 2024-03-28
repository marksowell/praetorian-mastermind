# Praetorian Mastermind

## Introduction
This repository contains the solution to the [Praetorian Tech Challenge - Mastermind](https://www.praetorian.com/challenges/mastermind/). It includes a Python-based interface for interacting with the challenge's API, managing game states, and algorithmically solving the Mastermind game.

## Features

- **API Interaction**: Automates requests to the Mastermind game API for game state management, level progression, and guess submission.
- **Algorithmic Solving**: Employs strategies to efficiently solve levels, including permutation and combination logic.
- **Performance Metrics**: Displays the time taken and the number of guesses required to solve each level, providing insights into the algorithm's efficiency.
- **Multiprocessing**: Utilizes Python's multiprocessing capabilities to leverage multiple CPU cores for faster computation and solution finding.

## Installation

To use this project, you'll need Python 3.x installed on your machine. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/marksowell/praetorian-mastermind.git
cd praetorian-mastermind
pip install -r requirements.txt
```

## Configuration
Before running the scripts, update interface.py with your email address to authenticate with the game's API:

```python
email = 'your_email@example.com'
```

## Usage

### Interface
The `interface.py` script provides functions to interact with the game's API, including resetting the game state, fetching the current level, and submitting guesses.

### Mastermind Solver
`mastermind.py` is the main script that utilizes multiprocessing and various algorithms to efficiently solve the Mastermind challenge.

To run the solver:
```bash
python mastermind.py
```
## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues to discuss potential improvements or report bugs.

## Acknowledgements

This project was inspired by and adapted from code found in the following repository: [praetorian_challenges/mastermind by choltz95](https://github.com/choltz95/praetorian_challenges/tree/master/mastermind).
