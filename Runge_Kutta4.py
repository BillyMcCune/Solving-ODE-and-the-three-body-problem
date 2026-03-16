import numpy as np
from method import Method


class RungeKutta4(Method):
    def next_step(self, f, t: float, y: np.ndarray, h: float) -> np.ndarray:
        k1 = f(t, y)
        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t + h, y + h * k3)
        return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
