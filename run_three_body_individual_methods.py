from pathlib import Path

from methods_registry import MethodName
from three_body_visual import run_three_body_plots


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

OUTPUT_DIR = Path("three_body_individual_method_plots")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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

            run_three_body_plots(
                step_hours=step_hours,
                duration_years=duration_years,
                method_name=method_name,
                compare_methods=False,
                output_dir=OUTPUT_DIR,
                show_plots=False,
            )

            run_index += 1


if __name__ == "__main__":
    main()
