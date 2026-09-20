#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Forward-Kinematics
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from forward_kinematics import TwoLinkForwardKinematics


robot = TwoLinkForwardKinematics(
    l1=1.0,
    l2=0.7,
)

time = np.linspace(
    0.0,
    10.0,
    500,
)

q1 = 0.8 * np.sin(time)
q2 = 0.6 * np.cos(0.7 * time)

path = []

for i in range(time.size):
    q = np.array([
        q1[i],
        q2[i],
    ])

    path.append(
        robot.position(q)
    )

path = np.asarray(path)

final_q = np.array([
    q1[-1],
    q2[-1],
])

joint_1, joint_2, end_effector = (
    robot.joint_positions(final_q)
)

plt.figure()

plt.plot(
    path[:, 0],
    path[:, 1],
    label="End-Effector Path",
)

plt.plot(
    [
        joint_1[0],
        joint_2[0],
        end_effector[0],
    ],
    [
        joint_1[1],
        joint_2[1],
        end_effector[1],
    ],
    marker="o",
    label="Final Configuration",
)

plt.axis("equal")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Two-Link Forward Kinematics")
plt.grid()
plt.legend()

plt.show()
