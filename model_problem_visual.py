import numpy as np
import matplotlib.pyplot as plt
from methods_registry import get_method_classes


def _run_method(method, f, t0, y0, h, steps):
    times = [t0]
    states = [y0.copy()]
    t = t0
    y = y0.copy()

    for _ in range(steps):
        y = method.next_step(f, t, y, h)
        t += h
        times.append(t)
        states.append(y.copy())

    return np.array(times), np.array(states)


def _sho_rhs(_t, y):
    #y = [position, velocity]
    return np.array([y[1], -y[0]], dtype=float)


def _pendulum_rhs(_t, y):
    #y = [angle, angular_velocity]
    return np.array([y[1], -np.sin(y[0])], dtype=float)


def _sho_energy(states):
    x = states[:, 0]
    v = states[:, 1]
    return 0.5 * (v * v + x * x)


def _pendulum_energy(states):
    theta = states[:, 0]
    omega = states[:, 1]
    return 0.5 * omega * omega + (1.0 - np.cos(theta))


def run_model_problem_plots(y0=1.0, h=0.01, steps=2000):
    method_classes = get_method_classes()

    #simple Harmonic Oscillator
    plt.figure()
    for method_name, cls in method_classes.items():
        method = cls()
        times, states = _run_method(method, _sho_rhs, 0.0, np.array([y0, 0.0]), h, steps)
        energy = _sho_energy(states)
        plt.plot(times, energy, label=method_name.value)
    plt.title("SHO Energy vs Time")
    plt.xlabel("Time")
    plt.ylabel("Energy")
    plt.legend()

    #pendulum
    plt.figure()
    for method_name, cls in method_classes.items():
        method = cls()
        times, states = _run_method(method, _pendulum_rhs, 0.0, np.array([y0, 0.0]), h, steps)
        energy = _pendulum_energy(states)
        plt.plot(times, energy, label=method_name.value)
    plt.title("Pendulum Energy vs Time")
    plt.xlabel("Time")
    plt.ylabel("Energy")
    plt.legend()

    plt.show()



run_model_problem_plots()
