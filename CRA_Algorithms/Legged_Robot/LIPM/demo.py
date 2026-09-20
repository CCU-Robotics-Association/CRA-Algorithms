#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : LIPM
@ Description        : demo
@ Author             : XCrane
"""


import numpy as np
import matplotlib.pyplot as plt
from lipm import LinearInvertedPendulum


model = LinearInvertedPendulum(
    com_height=0.8,
)

dt = 0.005
simulation_time = 3.0

time = np.arange(
    0.0,
    simulation_time,
    dt,
)

state = np.array([
    0.08,
    0.0,
])

support_point = 0.0

position_history = []
velocity_history = []
capture_point_history = []

for _ in time:
    position_history.append(
        state[0]
    )

    velocity_history.append(
        state[1]
    )

    capture_point_history.append(
        model.capture_point(
            state[0],
            state[1],
        )
    )

    state = model.step(
        state,
        dt,
        support_point=support_point,
    )

plt.figure()

plt.plot(
    time,
    position_history,
    label="CoM Position",
)

plt.plot(
    time,
    capture_point_history,
    label="Capture Point",
)

plt.axhline(
    support_point,
    linestyle="--",
    label="Support Point",
)

plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Linear Inverted Pendulum Model")
plt.grid()
plt.legend()

plt.show()
