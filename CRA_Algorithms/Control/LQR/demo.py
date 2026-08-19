#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : LQR
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from lqr import lqr

A = np.array([
    [0.0, 1.0],
    [0.0, 0.0],
])

B = np.array([
    [0.0],
    [1.0],
])

Q = np.array([
    [10.0, 0.0],
    [0.0, 1.0],
])

R = np.array([
    [1.0],
])

K, P, eigenvalues = lqr(
    A,
    B,
    Q,
    R,
)

print(f"K:{K}")
print(f"P:{P}")
print(f"Closed-loop eigenvalues:{eigenvalues}")
dt = 0.01
simulation_time = 10.0
steps = int(simulation_time / dt)
state = np.array([
    [5.0],
    [0.0],
])
time_history = []
position_history = []
velocity_history = []
control_history = []

for i in range(steps):
    t = i * dt
    u = -K @ state
    state_dot = (
        A @ state
        +
        B @ u
    )
    state += state_dot * dt
    time_history.append(t)
    position_history.append(state[0, 0])
    velocity_history.append(state[1, 0])
    control_history.append(u[0, 0])

plt.plot(
    time_history,
    position_history,
    label="Position",
)

plt.plot(
    time_history,
    velocity_history,
    label="Velocity",
)

plt.axhline(
    0,
    linestyle="--",
    label="Target",
)

plt.xlabel("Time (s)")
plt.ylabel("State")
plt.title("LQR Control")
plt.grid()
plt.legend()
plt.show()