import numpy as np
from method import Method


class VelocityVerlet(Method):
    def next_step(self, f, t: float, y: np.ndarray, h: float) -> np.ndarray:
        # f returns [velocity, acceleration]
        # y = [position, velocity]

        n = len(y) // 2
        
        r = y[:n]
        v = y[n:]   

        current_f = f(t, y)
        a = current_f[n:]

        r_next = r + h*v + 0.5 * a * h * h

        # Only valid when a(t+h) depends only on position
        y_temp = np.concatenate([r_next, v])
        next_f = f(t+h, y_temp)
        a_next = next_f[n:]

        v_next = v + 0.5 * h * (a + a_next)


        return np.concatenate([r_next, v_next])
