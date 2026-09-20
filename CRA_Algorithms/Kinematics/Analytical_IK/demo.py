#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Analytical-IK
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from analytical_ik import TwoLinkAnalyticalIK


solver = TwoLinkAnalyticalIK(
    l1=1.0,
    l2=0.7,
)

target = np.array([
    1.0,
    0.8,
])

solutions = {
    "Elbow Up": solver.solve(
        target,
        elbow="up",
    ),
    "Elbow Down": solver.solve(
        target,
        elbow="down",
    ),
}

plt.figure()

for label, q in solutions.items():
    q1, q2 = q

    joint_2 = np.array([
        solver.l1 * np.cos(q1),
        solver.l1 * np.sin(q1),
    ])

    end_effector = joint_2 + np.array([
        solver.l2 * np.cos(q1 + q2),
        solver.l2 * np.sin(q1 + q2),
    ])

    plt.plot(
        [
            0.0,
            joint_2[0],
            end_effector[0],
        ],
        [
            0.0,
            joint_2[1],
            end_effector[1],
        ],
        marker="o",
        label=label,
    )

plt.scatter(
    target[0],
    target[1],
    marker="x",
    s=100,
    label="Target",
)

plt.axis("equal")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Two-Link Analytical Inverse Kinematics")
plt.grid()
plt.legend()

plt.show()
