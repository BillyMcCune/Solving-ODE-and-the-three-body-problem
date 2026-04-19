import numpy as np
from method import Method


class AdamsBashforth(Method):
    def __init__(self):
        self.prev_f = None
        self.startup_steps = 2
        self.startup_steps_done = 0

    def next_step(self, f, t: float, y: np.ndarray, h: float) -> np.ndarray:
        current_f = f(t, y)

        if self.startup_steps_done < self.startup_steps:
            # Use second-order trapezoid startup steps before switching to AB2.
            y_predict = y + h * current_f
            f_predict = f(t + h, y_predict)
            y_next = y + 0.5 * h * (current_f + f_predict)
        else:
            y_next = y + h * (1.5 * current_f - 0.5 * self.prev_f)

        self.prev_f = current_f
        self.startup_steps_done += 1
        return y_next


