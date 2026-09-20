#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Forward-Dynamics
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt

from Dynamics.Forward_Dynamics.forward_dynamics import TwoLinkForwardDynamics


model = TwoLinkForwardDynamics()

q1 = 0.0
dq1 = 0.0

q2_values = np.linspace(
    -np.pi,
    np.pi,
    500,
)

tau = np.array([
    10.0,
    2.0,
])

ddq_history = []

for q2 in q2_values:
    q = np.array([
        q1,
        q2,
    ])

    dq = np.array([
        dq1,
        0.0,
    ])

    ddq = model.acceleration(
        q,
        dq,
        tau,
    )

    ddq_history.append(ddq)

ddq_history = np.asarray(
    ddq_history
)

plt.figure()

plt.plot(
    q2_values,
    ddq_history[:, 0],
    label="Joint 1 Acceleration",
)

plt.plot(
    q2_values,
    ddq_history[:, 1],
    label="Joint 2 Acceleration",
)

plt.xlabel("Joint 2 Angle (rad)")
plt.ylabel("Acceleration (rad/s²)")
plt.title("Two-Link Forward Dynamics")
plt.grid()
plt.legend()

plt.show()
