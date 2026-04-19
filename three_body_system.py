import numpy as np


class ThreeBodySystem:
    def __init__(
        self,
        m1: float,
        m2: float,
        m3: float,
        G: float = 6.6743e-11,
        length_scale: float = 1.0,
    ):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.G = G
        self.length_scale = length_scale

    def derivatives(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        y = [r1(3), r2(3), r3(3), v1(3), v2(3), v3(3)]
        returns dy/dt = [v1, v2, v3, a1, a2, a3]
        """
        r1 = y[0:3]
        r2 = y[3:6]
        r3 = y[6:9]
        v1 = y[9:12]
        v2 = y[12:15]
        v3 = y[15:18]

        def accel(ri, rj, mj):
            diff_si = self.length_scale * (rj - ri)
            dist_si = np.linalg.norm(diff_si)
            accel_si = self.G * mj * diff_si / dist_si**3
            return accel_si / self.length_scale

        a1 = accel(r1, r2, self.m2) + accel(r1, r3, self.m3)
        a2 = accel(r2, r1, self.m1) + accel(r2, r3, self.m3)
        a3 = accel(r3, r1, self.m1) + accel(r3, r2, self.m2)

        dydt = np.zeros_like(y)
        dydt[0:3] = v1
        dydt[3:6] = v2
        dydt[6:9] = v3
        dydt[9:12] = a1
        dydt[12:15] = a2
        dydt[15:18] = a3

        return dydt

    def total_energy(self, y: np.ndarray) -> float:
        r1 = self.length_scale * y[0:3]
        r2 = self.length_scale * y[3:6]
        r3 = self.length_scale * y[6:9]
        v1 = self.length_scale * y[9:12]
        v2 = self.length_scale * y[12:15]
        v3 = self.length_scale * y[15:18]

        kinetic = (
            0.5 * self.m1 * np.dot(v1, v1)
            + 0.5 * self.m2 * np.dot(v2, v2)
            + 0.5 * self.m3 * np.dot(v3, v3)
        )

        d12 = np.linalg.norm(r2 - r1)
        d13 = np.linalg.norm(r3 - r1)
        d23 = np.linalg.norm(r3 - r2)

        potential = -self.G * (
            self.m1 * self.m2 / d12
            + self.m1 * self.m3 / d13
            + self.m2 * self.m3 / d23
        )

        return kinetic + potential
