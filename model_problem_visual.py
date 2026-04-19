import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from methods_registry import MethodName, get_method_classes


def _set_window_title(fig, title):
    manager = getattr(fig.canvas, "manager", None)
    if manager is not None and hasattr(manager, "set_window_title"):
        manager.set_window_title(title)


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


def _plain_tick_label(value, _pos):
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _format_energy_axis(ax):
    ax.yaxis.set_major_formatter(FuncFormatter(_plain_tick_label))


def _plot_individual_method_results(problem_name, times, energy, method_name):
    fig, ax = plt.subplots()
    title = f"{problem_name} Energy vs Time ({method_name.value})"
    ax.plot(times, energy, label=method_name.value)
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("Energy")
    ax.legend()
    _format_energy_axis(ax)
    _set_window_title(fig, title)
    return fig, ax


def run_model_problem_plots(y0=1.0, h=0.01, steps=2000):
    available_methods = get_method_classes()
    plot_methods = [
        MethodName.ADAMS_BASHFORTH,
        # MethodName.ADAMS_MOULTON,
        MethodName.RUNGE_KUTTA4,
        MethodName.VELOCITY_VERLET,
    ]
    method_classes = {method: available_methods[method] for method in plot_methods}

    #simple Harmonic Oscillator
    sho_fig, sho_ax = plt.subplots()
    for method_name, cls in method_classes.items():
        method = cls()
        times, states = _run_method(method, _sho_rhs, 0.0, np.array([y0, 0.0]), h, steps)
        energy = _sho_energy(states)
        sho_ax.plot(times, energy, label=method_name.value)
        _plot_individual_method_results("SHO", times, energy, method_name)
    sho_title = "SHO Energy vs Time"
    sho_ax.set_title(sho_title)
    sho_ax.set_xlabel("Time")
    sho_ax.set_ylabel("Energy")
    sho_ax.legend()
    _format_energy_axis(sho_ax)
    _set_window_title(sho_fig, sho_title)

    #pendulum
    pendulum_fig, pendulum_ax = plt.subplots()
    for method_name, cls in method_classes.items():
        method = cls()
        times, states = _run_method(method, _pendulum_rhs, 0.0, np.array([y0, 0.0]), h, steps)
        energy = _pendulum_energy(states)
        pendulum_ax.plot(times, energy, label=method_name.value)
        _plot_individual_method_results("Pendulum", times, energy, method_name)
    pendulum_title = "Pendulum Energy vs Time"
    pendulum_ax.set_title(pendulum_title)
    pendulum_ax.set_xlabel("Time")
    pendulum_ax.set_ylabel("Energy")
    pendulum_ax.legend()
    _format_energy_axis(pendulum_ax)
    _set_window_title(pendulum_fig, pendulum_title)

    plt.show()

if __name__ == "__main__":
    run_model_problem_plots()
