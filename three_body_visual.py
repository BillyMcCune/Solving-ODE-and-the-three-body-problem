import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from space_object import SpaceObject
from three_body_system import ThreeBodySystem
from simulation_runner import SimulationRunner
from methods_registry import MethodName, get_method_classes


def _build_default_system():
    r_sun = SpaceObject([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 1.989e30)
    r_earth = SpaceObject([1.496e11, 0.0, 0.0], [0.0, 2.978e4, 0.0], 5.972e24)
    r_moon = SpaceObject(
        [1.496e11 + 3.844e8, 0.0, 0.0],
        [0.0, 2.978e4 + 1.022e3, 0.0],
        7.35e22,
    )

    system = ThreeBodySystem(r_sun.mass, r_earth.mass, r_moon.mass)
    y0 = np.concatenate([
        r_sun.r, r_earth.r, r_moon.r,
        r_sun.v, r_earth.v, r_moon.v,
    ])

    return system, y0


def run_three_body_plots(
    h=3600 * 6,
    steps=4 * 365,
    method_name=MethodName.ADAMS_MOULTON,
    compare_methods=True,
):
    system, y0 = _build_default_system()

    if compare_methods:
        method_classes = get_method_classes()
    else:
        method_classes = {method_name: get_method_classes()[method_name]}

    plt.figure()
    plt.title("Total Energy vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Energy (J)")

    plt.figure()
    plt.title("Earth–Sun Distance vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")

    plt.figure()
    plt.title("Earth–Moon Distance vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")

    for method_key, method_cls in method_classes.items():
        runner = SimulationRunner(system, method_cls())
        times, states = runner.run(t0=0.0, y0=y0, h=h, steps=steps)

        energy = []
        earth_sun_dist = []
        earth_moon_dist = []

        for y in states:
            r1 = y[0:3]   # sun
            r2 = y[3:6]   # earth
            r3 = y[6:9]   # moon

            earth_sun_dist.append(np.linalg.norm(r2 - r1))
            earth_moon_dist.append(np.linalg.norm(r3 - r2))
            energy.append(system.total_energy(y))

        label = method_key.value if hasattr(method_key, "value") else str(method_key)

        plt.figure(1)
        plt.plot(times, energy, label=label)

        plt.figure(2)
        plt.plot(times, earth_sun_dist, label=label)

        plt.figure(3)
        plt.plot(times, earth_moon_dist, label=label)

    plt.figure(1)
    plt.legend()
    plt.figure(2)
    plt.legend()
    plt.figure(3)
    plt.legend()

    plt.show()


def animate_three_body(
    h=3600 * 6, steps=4 * 365, stride=4, method_name=MethodName.ADAMS_MOULTON
):
    system, y0 = _build_default_system()
    method_cls = get_method_classes()[method_name]
    runner = SimulationRunner(system, method_cls())

    times, states = runner.run(t0=0.0, y0=y0, h=h, steps=steps)
    states = states[::stride]
    times = times[::stride]

    sun = states[:, 0:3]
    earth = states[:, 3:6]
    moon = states[:, 6:9]

    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')

    max_extent = np.max(np.linalg.norm(earth[:, 0:2], axis=1)) * 1.2
    ax.set_xlim(-max_extent, max_extent)
    ax.set_ylim(-max_extent, max_extent)
    ax.set_title("Three-Body Simulation")

    sun_scatter = ax.scatter([], [], s=60, label="Sun")
    earth_scatter = ax.scatter([], [], s=20, label="Earth")
    moon_scatter = ax.scatter([], [], s=10, label="Moon")
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    ax.legend(loc="upper right")

    def init():
        sun_scatter.set_offsets(np.empty((0, 2)))
        earth_scatter.set_offsets(np.empty((0, 2)))
        moon_scatter.set_offsets(np.empty((0, 2)))
        time_text.set_text('')
        return sun_scatter, earth_scatter, moon_scatter, time_text

    def update(i):
        sun_scatter.set_offsets(sun[i, 0:2])
        earth_scatter.set_offsets(earth[i, 0:2])
        moon_scatter.set_offsets(moon[i, 0:2])
        time_text.set_text(f"t = {times[i]:.0f} s")
        return sun_scatter, earth_scatter, moon_scatter, time_text

    anim = FuncAnimation(fig, update, frames=len(times), init_func=init, blit=True, interval=30)
    plt.show()
    return anim



run_three_body_plots()
animate_three_body()
