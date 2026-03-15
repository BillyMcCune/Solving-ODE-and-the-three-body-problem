import numpy as np
from space_object import SpaceObject
from three_body_system import ThreeBodySystem
from simulation_runner import SimulationRunner
from Adams_Bashforth import AdamsBashforth
from Adams_Moulton import AdamsMoulton
import matplotlib.pyplot as plt

r_sun = SpaceObject([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 1.989e30)

r_earth = SpaceObject([1.496e11, 0.0, 0.0], [0.0, 2.978e4, 0.0], 5.972e24)

r_moon = SpaceObject(
    [1.496e11 + 3.844e8, 0.0, 0.0],
    [0.0, 2.978e4 + 1.022e3, 0.0],
    7.35e22
)

system = ThreeBodySystem(r_sun.mass, r_earth.mass, r_moon.mass)

y0 = np.concatenate([
    r_sun.r, r_earth.r, r_moon.r,
    r_sun.v, r_earth.v, r_moon.v
])

runner = SimulationRunner(system, AdamsMoulton())

times, states = runner.run(
    t0=0.0,
    y0=y0,
    h= 3600 * 6 ,
    steps= 4 * 365
)

print("Final state:")
print(states[-1])

print("Initial energy:", system.total_energy(states[0]))
print("Final energy:", system.total_energy(states[-1]))

energy = []
earth_sun_dist = []
earth_moon_dist = []

for y in states:

    r1 = y[0:3]   #sun
    r2 = y[3:6]   #earth
    r3 = y[6:9]   #moon

    earth_sun_dist.append(np.linalg.norm(r2 - r1))
    earth_moon_dist.append(np.linalg.norm(r3 - r2))

    energy.append(system.total_energy(y))

# energy
plt.plot(times, energy)
plt.title("Total Energy vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")

plt.show()
# the earth to the Sun Distance
plt.figure()

plt.plot(times, earth_sun_dist)
plt.title("Earth–Sun Distance vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Distance (m)")

plt.show()

# the earth to the moon distance
plt.figure()

plt.plot(times, earth_moon_dist)
plt.title("Earth–Moon Distance vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Distance (m)")

plt.show()
