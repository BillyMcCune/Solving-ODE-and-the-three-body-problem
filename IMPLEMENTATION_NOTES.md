# Implementation Notes

## Energy Units

- The three-body simulation energy is in joules.
- The model-problem energies are normalized, dimensionless energies.

## Simple Harmonic Oscillator

### Equation

`y'' = -y`

### State Representation

- State vector: `[position, velocity]`
- Implemented in `model_problem_visual.py` as:
  - `position = y[0]`
  - `velocity = y[1]`

### First-Order System

The second-order ODE is rewritten as:

- `x' = v`
- `v' = -x`

This is implemented by `_sho_rhs`.

### Energy

The normalized energy is:

`E = 0.5 * (v^2 + x^2)`

This is implemented by `_sho_energy`.

### Notes

- This model is used as a clean test problem because the exact behavior is simple and bounded.
- It is useful for comparing how well each method preserves energy over time.

## Pendulum

### Equation

`y'' = -sin(y)`

### State Representation

- State vector: `[angle, angular_velocity]`

### First-Order System

The second-order ODE is rewritten as:

- `theta' = omega`
- `omega' = -sin(theta)`

This is implemented by `_pendulum_rhs`.

### Energy

The normalized energy is:

`E = 0.5 * omega^2 + (1 - cos(theta))`

This is implemented by `_pendulum_energy`.

### Notes

- This is a nonlinear model, unlike the SHO.
- It is useful for seeing how the methods behave on a slightly harder conservative system.

## Three-Body Problem

### Physical System

The simulation models the Sun, Earth, and Moon in a planar Newtonian gravity setting.

### State Representation

The state vector has 18 entries:

- `[r1(3), r2(3), r3(3), v1(3), v2(3), v3(3)]`
- `r1`, `r2`, `r3` are the body positions
- `v1`, `v2`, `v3` are the body velocities

This is implemented in `three_body_system.py`.

### Units

- Masses are stored in kilograms.
- Gravitation uses the SI gravitational constant `G = 6.6743e-11`.
- The simulation state is stored in astronomical units for position and AU/s for velocity.
- A `length_scale` converts the AU-based state back to SI distances when computing forces and total energy.

### Equations

Each body's acceleration is computed from pairwise Newtonian gravity:

`a_i = sum_j G * m_j * (r_j - r_i) / |r_j - r_i|^3`

Internally:

- distances are converted from AU to meters before applying the gravity law
- accelerations are converted back into AU/s^2 before being returned to the integrator

### Energy

The total energy is:

- kinetic energy: `0.5 * m * |v|^2` summed over all bodies
- potential energy: `-G * m_i * m_j / r_ij` summed over body pairs

This total is returned in joules by `ThreeBodySystem.total_energy`.

### Initial Conditions

The default setup in `three_body_visual.py` uses:

- Sun at the origin
- Earth at `1 AU`
- Moon offset from Earth by its mean orbital distance
- velocities expressed in AU/s

### Notes

- Positions are plotted in AU.
- Time in the plots is shown in years.
- Energy stays in joules even though the state uses AU-based coordinates, because the energy calculation converts back to SI units.

## Time-Stepping Methods

### Adams-Bashforth 2

- Implemented in `Adams_Bashforth.py`
- Uses trapezoid startup steps before switching to the AB2 update
- The AB2 update is:

`y_(n+1) = y_n + h * (3/2 f_n - 1/2 f_(n-1))`

### Adams-Moulton / Trapezoid

- Implemented in `Adams_Moulton.py`
- Uses an Euler predictor and trapezoid corrector

### Runge-Kutta 4

- Implemented in `Runge_Kutta4.py`
- Used as a higher-order comparison method

### Velocity Verlet

- Implemented in `Velocity_Verlet.py`
- Intended for systems where acceleration depends on position
- Included as the symplectic method in the project
