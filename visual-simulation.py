from methods_registry import MethodName
from model_problem_visual import run_model_problem_plots
from three_body_visual import run_three_body_plots, animate_three_body


run_model_problem_plots(y0=1.0, h=0.01, steps=20000)
run_three_body_plots(step_hours=6.0,
    duration_years=20.0,
    method_name=MethodName.ADAMS_BASHFORTH,
    compare_methods=True,)
animate_three_body(method_name=MethodName.ADAMS_BASHFORTH, duration_years=1000, step_hours=10)

