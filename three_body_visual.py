import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FuncFormatter
from pathlib import Path
from space_object import SpaceObject
from three_body_system import ThreeBodySystem
from simulation_runner import SimulationRunner
from methods_registry import MethodName, get_method_classes

ASTRONOMICAL_UNIT_METERS = 1.495978707e11
SECONDS_PER_HOUR = 3600.0
HOURS_PER_YEAR = 365.25 * 24.0
SECONDS_PER_YEAR = HOURS_PER_YEAR * SECONDS_PER_HOUR


def _set_window_title(fig, title):
    manager = getattr(fig.canvas, "manager", None)
    if manager is not None and hasattr(manager, "set_window_title"):
        manager.set_window_title(title)


def _scientific_tick_label(value, _pos):
    return f"{value:.2e}"


def _years_label(duration_years: float) -> str:
    if float(duration_years).is_integer():
        return f"{int(duration_years)} years"
    return f"{duration_years:g} years"


def _slugify(text: str) -> str:
    return (
        text.lower()
        .replace("–", "-")
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
    )


def _simulation_grid(step_hours: float, duration_years: float) -> tuple[float, int]:
    if step_hours <= 0.0:
        raise ValueError("step_hours must be positive")
    if duration_years <= 0.0:
        raise ValueError("duration_years must be positive")

    h = step_hours * SECONDS_PER_HOUR
    steps = max(1, int(round(duration_years * HOURS_PER_YEAR / step_hours)))
    return h, steps


def _build_default_system():
    earth_orbit_au = 1.0
    moon_orbit_au = 3.844e8 / ASTRONOMICAL_UNIT_METERS
    earth_speed_au_per_s = 2.978e4 / ASTRONOMICAL_UNIT_METERS
    moon_speed_au_per_s = 1.022e3 / ASTRONOMICAL_UNIT_METERS

    r_sun = SpaceObject([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 1.989e30)
    r_earth = SpaceObject([earth_orbit_au, 0.0, 0.0], [0.0, earth_speed_au_per_s, 0.0], 5.972e24)
    r_moon = SpaceObject(
        [earth_orbit_au + moon_orbit_au, 0.0, 0.0],
        [0.0, earth_speed_au_per_s + moon_speed_au_per_s, 0.0],
        7.35e22,
    )

    system = ThreeBodySystem(
        r_sun.mass,
        r_earth.mass,
        r_moon.mass,
        length_scale=ASTRONOMICAL_UNIT_METERS,
    )
    y0 = np.concatenate([
        r_sun.r, r_earth.r, r_moon.r,
        r_sun.v, r_earth.v, r_moon.v,
    ])

    return system, y0


def run_three_body_plots(
    step_hours=24,
    duration_years=20.0,
    method_name=MethodName.ADAMS_BASHFORTH,
    compare_methods=True,
    output_dir=None,
    show_plots=True,
):
    system, y0 = _build_default_system()
    h, steps = _simulation_grid(step_hours, duration_years)

    available_methods = get_method_classes()
    if compare_methods:
        plot_methods = [
            MethodName.ADAMS_BASHFORTH,
            # MethodName.ADAMS_MOULTON,
            #MethodName.RUNGE_KUTTA4,
        #  MethodName.VELOCITY_VERLET,
        ]
        method_classes = {method: available_methods[method] for method in plot_methods}
    else:
        method_classes = {method_name: available_methods[method_name]}

    duration_label = _years_label(duration_years)
    title_suffix = f" ({duration_label}"
    if not compare_methods:
        title_suffix += f", {method_name.value}"
    title_suffix += ")"
    energy_title = f"Total Energy vs Time{title_suffix}"
    earth_sun_title = f"Earth–Sun Distance vs Time{title_suffix}"
    earth_moon_title = f"Earth–Moon Distance vs Time{title_suffix}"

    energy_fig, energy_ax = plt.subplots()
    energy_ax.set_title(energy_title)
    energy_ax.set_xlabel("Time (years)")
    energy_ax.set_ylabel("Energy (Joules)")
    _set_window_title(energy_fig, energy_title)

    earth_sun_fig, earth_sun_ax = plt.subplots()
    earth_sun_ax.set_title(earth_sun_title)
    earth_sun_ax.set_xlabel("Time (years)")
    earth_sun_ax.set_ylabel("Distance (AU)")
    _set_window_title(earth_sun_fig, earth_sun_title)

    earth_moon_fig, earth_moon_ax = plt.subplots()
    earth_moon_ax.set_title(earth_moon_title)
    earth_moon_ax.set_xlabel("Time (years)")
    earth_moon_ax.set_ylabel("Distance (AU)")
    _set_window_title(earth_moon_fig, earth_moon_title)

    for method_key, method_cls in method_classes.items():
        runner = SimulationRunner(system, method_cls())
        times, states = runner.run(t0=0.0, y0=y0, h=h, steps=steps)
        times_years = times / SECONDS_PER_YEAR

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

        energy_ax.plot(times_years, energy, label=label)
        earth_sun_ax.plot(times_years, earth_sun_dist, label=label)
        earth_moon_ax.plot(times_years, earth_moon_dist, label=label)

    energy_ax.legend()
    energy_ax.yaxis.set_major_formatter(FuncFormatter(_scientific_tick_label))
    earth_sun_ax.legend()
    earth_moon_ax.legend()

    if output_dir is not None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        figures = [
            (energy_fig, energy_title),
            (earth_sun_fig, earth_sun_title),
            (earth_moon_fig, earth_moon_title),
        ]

        for fig, title in figures:
            fig.savefig(output_path / f"{_slugify(title)}.png", dpi=200, bbox_inches="tight")

    if show_plots:
        plt.show()
    else:
        plt.close(energy_fig)
        plt.close(earth_sun_fig)
        plt.close(earth_moon_fig)


def animate_three_body(
    step_hours=12.0,
    duration_years=1.0,
    frame_stride=10,
    method_name=MethodName.VELOCITY_VERLET,
):
    system, y0 = _build_default_system()
    method_cls = get_method_classes()[method_name]
    runner = SimulationRunner(system, method_cls())
    h, steps = _simulation_grid(step_hours, duration_years)

    times, states = runner.run(t0=0.0, y0=y0, h=h, steps=steps)
    states = states[::frame_stride]
    times = times[::frame_stride]
    times_years = times / SECONDS_PER_YEAR

    sun = states[:, 0:3]
    earth = states[:, 3:6]
    moon = states[:, 6:9]

    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')

    max_extent = np.max(np.linalg.norm(earth[:, 0:2], axis=1)) * 1.2
    ax.set_xlim(-max_extent, max_extent)
    ax.set_ylim(-max_extent, max_extent)
    ax.set_title(f"Three-Body Simulation ({method_name.value})")
    ax.set_xlabel("x (AU)")
    ax.set_ylabel("y (AU)")
    _set_window_title(fig, f"Three-Body Simulation ({method_name.value})")

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
        time_text.set_text(f"t = {times_years[i]:.2f} years")
        return sun_scatter, earth_scatter, moon_scatter, time_text

    anim = FuncAnimation(fig, update, frames=len(times), init_func=init, blit=True, interval=30)
    plt.show()
    return anim

if __name__ == "__main__":
    run_three_body_plots()
    animate_three_body()
