#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : SMO
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from smc import SuperTwistingObserver

dt = 0.01
simulation_time = 10.0
frequency = 0.5
noise_std = 0.1

time = np.arange(
    0.0,
    simulation_time,
    dt,
)

true_position = np.sin(
    2.0 * np.pi * frequency * time
)

true_velocity = (
    2.0
    * np.pi
    * frequency
    * np.cos(
        2.0 * np.pi * frequency * time
    )
)

rng = np.random.default_rng(0)

measurement = (
    true_position
    + noise_std
    * rng.standard_normal(time.size)
)

observer = SuperTwistingObserver(
    k1=5.0,
    k2=20.0,
    dt=dt,
)

estimated_position = []
estimated_velocity = []

for value in measurement:
    position_hat, velocity_hat = observer.update(
        value
    )

    estimated_position.append(
        position_hat
    )

    estimated_velocity.append(
        velocity_hat
    )

plt.figure()

plt.plot(
    time,
    true_position,
    label="True Position",
)

plt.plot(
    time,
    measurement,
    label="Measurement",
    alpha=0.5,
)

plt.plot(
    time,
    estimated_position,
    label="Estimated Position",
)

plt.xlabel("Time (s)")
plt.ylabel("Position")
plt.title("Super-Twisting Observer - Position")
plt.grid()
plt.legend()

plt.figure()

plt.plot(
    time,
    true_velocity,
    label="True Velocity",
)

plt.plot(
    time,
    estimated_velocity,
    label="Estimated Velocity",
)

plt.xlabel("Time (s)")
plt.ylabel("Velocity")
plt.title("Super-Twisting Observer - Velocity")
plt.grid()
plt.legend()

plt.show()
