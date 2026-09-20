#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : RNEA
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from Dynamics.RNEA.rnea import TwoLinkRNEA

model = TwoLinkRNEA()

dt = 0.01
simulation_time = 10.0

time = np.arange(
    0.0,
    simulation_time,
    dt,
)

q1 = 0.5 * np.sin(time)
q2 = 0.4 * np.cos(0.7 * time)

dq1 = 0.5 * np.cos(time)
dq2 = -0.28 * np.sin(0.7 * time)

ddq1 = -0.5 * np.sin(time)
ddq2 = -0.196 * np.cos(0.7 * time)

tau_history = []

for i in range(time.size):
    q = np.array([
        q1[i],
        q2[i],
    ])

    dq = np.array([
        dq1[i],
        dq2[i],
    ])

    ddq = np.array([
        ddq1[i],
        ddq2[i],
    ])

    tau = model.inverse_dynamics(
        q,
        dq,
        ddq,
    )

    tau_history.append(tau)

tau_history = np.asarray(
    tau_history
)

plt.figure()

plt.plot(
    time,
    tau_history[:, 0],
    label="Joint 1 Torque",
)

plt.plot(
    time,
    tau_history[:, 1],
    label="Joint 2 Torque",
)

plt.xlabel("Time (s)")
plt.ylabel("Torque (N·m)")
plt.title("Recursive Newton-Euler Inverse Dynamics")
plt.grid()
plt.legend()

plt.show()
