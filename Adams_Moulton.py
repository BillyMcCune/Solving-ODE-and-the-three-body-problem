import numpy as np
from method import Method


class AdamsMoulton(Method):
    def next_step(self, f, t: float, y: np.ndarray, h: float) -> np.ndarray:
        current_f = f(t, y)

        #Euler
        y_predict = y + h * current_f

        f_predict = f(t + h, y_predict)
        y_next = y + (h / 2.0) * (current_f + f_predict)

        return y_next