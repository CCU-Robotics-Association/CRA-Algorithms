#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Raibert-Controller
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from raibert import RaibertFootPlacement

controller = RaibertFootPlacement(
    stance_time=0.25,
    velocity_gain=0.18,
)

time = np.linspace(
    0.0,
    8.0,
    400,
)

desired_velocity = np.array([
    1.0,
    0.0,
])

current_velocity_x = (
    1.0
    + 0.5
    * np.sin(
        2.0
        * np.pi
        * 0.3
        * time
    )
)

foot_x = []

for velocity_x in current_velocity_x:
    placement = controller.compute(
        np.array([
            velocity_x,
            0.0,
        ]),
        desired_velocity,
    )

    foot_x.append(
        placement[0]
    )

plt.figure()

plt.plot(
    time,
    current_velocity_x,
    label="Current Velocity",
)

plt.axhline(
    desired_velocity[0],
    linestyle="--",
    label="Desired Velocity",
)

plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Raibert Velocity Tracking Input")
plt.grid()
plt.legend()

plt.figure()

plt.plot(
    time,
    foot_x,
    label="Foot Placement",
)

plt.xlabel("Time (s)")
plt.ylabel("Foot Placement (m)")
plt.title("Raibert Foot Placement")
plt.grid()
plt.legend()

plt.show()
