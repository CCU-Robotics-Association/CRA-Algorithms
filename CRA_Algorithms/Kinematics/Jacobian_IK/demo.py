#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Jacobian-IK
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from jacobian_ik import TwoLinkJacobianIK

solver = TwoLinkJacobianIK(
    l1=1.0,
    l2=0.7,
    damping=0.05,
    step_size=0.8,
    tolerance=1e-5,
    max_iterations=200,
)

target = np.array([
    1.0,
    0.8,
])

initial_q = np.array([
    0.1,
    0.1,
])

q, iterations, history = solver.solve(
    target,
    initial_q=initial_q,
)

q1, q2 = q

joint_2 = np.array([
    solver.l1 * np.cos(q1),
    solver.l1 * np.sin(q1),
])

end_effector = solver.position(q)

print("Solution:")
print(q)

print("Iterations:")
print(iterations)

print("Final Error:")
print(
    np.linalg.norm(
        target - end_effector
    )
)

plt.figure()

plt.plot(
    history[:, 0],
    history[:, 1],
    marker=".",
    label="Iteration Path",
)

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
    label="Final Configuration",
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
plt.title("Damped Least-Squares Jacobian IK")
plt.grid()
plt.legend()

plt.show()
