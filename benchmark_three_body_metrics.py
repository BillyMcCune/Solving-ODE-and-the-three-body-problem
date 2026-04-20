from __future__ import annotations

import csv
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from methods_registry import MethodName, get_method_classes
from simulation_runner import SimulationRunner
from three_body_visual import _build_default_system, _simulation_grid


RUN_CONFIGS = [
    {"duration_years": 2.0, "step_hours": 6.0},
    {"duration_years": 20.0, "step_hours": 24.0},
    {"duration_years": 200.0, "step_hours": 24.0},
    {"duration_years": 2000.0, "step_hours": 24.0},
    {"duration_years": 20000.0, "step_hours": 240.0},
    {"duration_years": 200000.0, "step_hours": 240.0},
]

METHODS = [
    MethodName.ADAMS_BASHFORTH,
    MethodName.ADAMS_MOULTON,
    MethodName.RUNGE_KUTTA4,
    MethodName.VELOCITY_VERLET,
]

OUTPUT_DIR = Path("three_body_metric_benchmarks")


def _benchmark_run(method_name: MethodName, duration_years: float, step_hours: float) -> dict:
    system, y0 = _build_default_system()
    method_cls = get_method_classes()[method_name]
    runner = SimulationRunner(system, method_cls())
    h, steps = _simulation_grid(step_hours, duration_years)

    start = time.perf_counter()
    _times, states = runner.run(t0=0.0, y0=y0, h=h, steps=steps)
    runtime_seconds = time.perf_counter() - start

    energies = np.array([system.total_energy(state) for state in states], dtype=float)
    initial_energy = energies[0]
    relative_drift = np.abs((energies - initial_energy) / initial_energy)

    return {
        "method": method_name.value,
        "duration_years": duration_years,
        "step_hours": step_hours,
        "steps": steps,
        "runtime_seconds": runtime_seconds,
        "final_relative_energy_drift": float(relative_drift[-1]),
        "max_relative_energy_drift": float(np.max(relative_drift)),
    }


def _write_csv(results: list[dict], output_dir: Path) -> None:
    csv_path = output_dir / "three_body_runtime_energy_metrics.csv"
    fieldnames = [
        "method",
        "duration_years",
        "step_hours",
        "steps",
        "runtime_seconds",
        "final_relative_energy_drift",
        "max_relative_energy_drift",
    ]

    with csv_path.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def _plot_metric(results: list[dict], metric_key: str, ylabel: str, filename: str, title: str) -> None:
    fig, ax = plt.subplots()

    for method_name in METHODS:
        method_results = [row for row in results if row["method"] == method_name.value]
        durations = [row["duration_years"] for row in method_results]
        values = [row[metric_key] for row in method_results]
        ax.plot(durations, values, marker="o", label=method_name.value)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Simulation Duration (years)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    fig.savefig(OUTPUT_DIR / filename, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    total_runs = len(RUN_CONFIGS) * len(METHODS)
    run_index = 1

    for config in RUN_CONFIGS:
        duration_years = config["duration_years"]
        step_hours = config["step_hours"]

        for method_name in METHODS:
            print(
                f"[{run_index}/{total_runs}] "
                f"{method_name.value}: duration_years={duration_years}, step_hours={step_hours}"
            )
            results.append(_benchmark_run(method_name, duration_years, step_hours))
            run_index += 1

    _write_csv(results, OUTPUT_DIR)
    _plot_metric(
        results,
        metric_key="runtime_seconds",
        ylabel="Runtime (seconds)",
        filename="runtime_vs_duration.png",
        title="Three-Body Runtime vs Duration",
    )
    _plot_metric(
        results,
        metric_key="max_relative_energy_drift",
        ylabel="Max Relative Energy Drift",
        filename="max_energy_drift_vs_duration.png",
        title="Three-Body Max Energy Drift vs Duration",
    )
    _plot_metric(
        results,
        metric_key="final_relative_energy_drift",
        ylabel="Final Relative Energy Drift",
        filename="final_energy_drift_vs_duration.png",
        title="Three-Body Final Energy Drift vs Duration",
    )


if __name__ == "__main__":
    main()
