This is extremely simplified Python version of the Java code of my Master's thesis. The point for it was to teach me pandas-usage as well as showcase my current proficiency in Python.

The application tries to predict (NHL) hockey games outcomes (home win, draw, away win) using Poisson distribution of scored goals by both teams in three past games. User can choose what season's games are used in simulation. After the simulation application shows the results of the simulation.

Quite extenive set of tests is also included.


Python packages scipy.stats and pandas need to be installed, in order to run the code.

Application was created with Python 3.7 in Mac OSX environment.

To run the code input:
`python app.py`

To run the tests:
`python -m unittest test_functions.py`
