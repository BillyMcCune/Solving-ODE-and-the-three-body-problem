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
- `python3 run_three_body_individual_methods.py` runs three-body plots for each method over the requested year/step-size sweep and saves them in `three_body_individual_method_plots/`.
- `python3 benchmark_three_body_metrics.py` benchmarks three-body runtime and energy drift, then saves a CSV and plots in `three_body_metric_benchmarks/`.
- `python3 save_three_body_video.py --output three_body.mp4` saves the three-body animation directly to video.
- `python3 make_three_body_video.py` is the simple one-click video export script with editable defaults at the top of the file.

# Documentation
- See [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) for implementation notes, model definitions, and energy-unit details.

# Three-body defaults
- `run_three_body_plots(step_hours=6.0, duration_years=2.0, ...)` uses a 6-hour step over 2 years.
- `animate_three_body(step_hours=12.0, duration_years=1.0, frame_stride=10, ...)` uses a 12-hour step over 1 year.

# Methods
- Adams-Bashforth (2nd order)
- Adams-Moulton (2nd order)
- Runge-Kutta 4 (comparison baseline)
