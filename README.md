# Solving-ODE-and-the-three-body-problem
Trying out 2 different numerical methods for solving the three-body problem 

A Multistep methods 2nd order - Billy
B Symplectic methods 2nd order - Jake Wolfram 

# Full problem:
 Using Newton's law of universal gravitation, we will model the Earth-
Moon-Sun system, which for simplicity can be taken to be in the z = 0 plane. Our code
should plot the following quantities over time
• The total energy
• The distance between the Earth and the Sun
• The distance between the Moon and the Earth
If we have time, I would also like the code to animate the current position of each celestial
body. 

Model problem: There are two model problems, though the second one's exact solution
is quite tricky to work with so use the first for testing. For both physical models, plot the
total energy. The two physical systems are

y′′ = −y, y(0) = y_0, y′(0) = 0, the simple harmonic oscillator,
y′′ = − sin(y) y(0) = y_0, y′(0) = 0, the pendulum.

# How to run
- `python3 visual-simulation.py` runs model problem energy plots (SHO and pendulum).
- `python3 visual-simulation.py` runs three-body energy + distance plots.
- `python3 visual-simulation.py` runs three-body animation via `FuncAnimation`.

# Methods
- Adams-Bashforth (2nd order)
- Adams-Moulton (2nd order)
- Runge-Kutta 4 (comparison baseline)
