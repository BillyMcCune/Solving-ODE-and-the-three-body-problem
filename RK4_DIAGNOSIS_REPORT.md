# RK4 Long-Run Instability Report

## Summary

The most likely reason the Runge-Kutta 4 plots "explode" is not a coding mistake in the RK4 update itself. The more plausible issue is long-term numerical instability from using a non-symplectic fixed-step method on a very long gravitational simulation.

In this project, that means:

- `RK4` is accurate locally but does not preserve the geometric structure of orbital motion over very long times.
- The three-body force law contains a `1 / r^3` term, so numerical drift can eventually create a near-collision or very close encounter.
- Once that happens, the acceleration becomes extremely large and a single step can throw the solution far off the physical orbit.
- On a plot, that shows up as a sudden jump or "explosion."

## What Was Checked

This diagnosis is based on code inspection and the run settings currently in the project. No code changes were made as part of this write-up.

### RK4 Implementation

The RK4 method in [Runge_Kutta4.py](/Users/billym./NumericalAnalysis/Solving-ODE-and-the-three-body-problem/Runge_Kutta4.py:5) is the standard classical fourth-order Runge-Kutta method:

```python
k1 = f(t, y)
k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
k4 = f(t + h, y + h * k3)
return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
```

There is no obvious implementation error in that file.

### Three-Body Force Model

The acceleration in [three_body_system.py](/Users/billym./NumericalAnalysis/Solving-ODE-and-the-three-body-problem/three_body_system.py:31) is computed with Newtonian gravity:

`a ~ (r_j - r_i) / |r_j - r_i|^3`

That means:

- if two bodies get too close numerically, the denominator gets very small
- the acceleration grows very quickly
- the problem becomes extremely stiff locally, even if the overall orbit had looked stable before

This makes long-run fixed-step integration fragile once drift pushes the system into a bad configuration.

### Long-Run Batch Settings

The batch driver in [run_three_body_individual_methods.py](/Users/billym./NumericalAnalysis/Solving-ODE-and-the-three-body-problem/run_three_body_individual_methods.py:6) runs:

- `2` years with `6` hour steps
- `20`, `200`, `2000` years with `24` hour steps
- `20000`, `200000` years with `240` hour steps

Those are very long horizons for a fixed-step non-symplectic method in a gravitational problem.

## Likely Cause

The likely cause is:

`RK4 + fixed step size + very long integration time + inverse-square gravitational singularity`

More concretely:

1. RK4 accumulates small long-term drift in invariants such as energy and orbital phase.
2. Over enough simulated years, that drift changes the orbit qualitatively.
3. A close encounter can then occur.
4. The `1 / r^3` force term makes the acceleration spike.
5. The trajectory becomes numerically unstable and the plot appears to blow up.

## Why Velocity Verlet Is Less Likely To Do This

This project also includes Velocity Verlet in [Velocity_Verlet.py](/Users/billym./NumericalAnalysis/Solving-ODE-and-the-three-body-problem/Velocity_Verlet.py:5).

Velocity Verlet is a symplectic method, which makes it better suited for long-time conservative orbital simulations. Even if its local order is lower than RK4, it often behaves better over very long horizons because it preserves the qualitative structure of the motion more faithfully.

So it is not surprising if:

- RK4 looks very good over short and medium times
- Velocity Verlet looks more physically stable over very long times

## Important Distinction

This report does **not** prove that the current RK4 trajectory failure is solely due to long-time drift, because I have not yet completed a full numerical diagnostic run comparing methods and measuring the failure point.

It does show that:

- the RK4 formula itself appears standard
- the force model has a singularity mechanism that can amplify drift dramatically
- the batch script uses time horizons where this kind of failure is plausible

## Recommended Diagnostic Next Steps

If you want to confirm the issue before making any changes, the next steps should be diagnostic only:

1. Measure relative energy drift for RK4 and Velocity Verlet at `20`, `200`, `2000`, and `20000` years.
2. Identify the first duration where RK4 loses qualitative orbital stability.
3. Track Earth-Sun and Earth-Moon distances to see whether the failure coincides with a close encounter.
4. Check whether reducing the RK4 step size delays the explosion.

## Conclusion

The current best diagnosis is that RK4 is not "broken" in the sense of having an obvious implementation error. The more likely problem is that it is being pushed into a regime where a non-symplectic fixed-step method becomes unreliable for long-time three-body integration.
