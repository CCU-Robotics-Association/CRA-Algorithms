#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : ZMP
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from zmp import ZMPCalculator

calculator = ZMPCalculator(
    com_height=0.8,
)

time = np.linspace(
    0.0,
    8.0,
    800,
)

omega = 2.0 * np.pi * 0.4

com_x = 0.03 * np.sin(
    omega * time
)

com_y = 0.02 * np.sin(
    0.5 * omega * time
)

com_ddx = (
    -0.03
    * omega**2
    * np.sin(
        omega * time
    )
)

com_ddy = (
    -0.02
    * (0.5 * omega)**2
    * np.sin(
        0.5 * omega * time
    )
)

zmp_history = []

for i in range(time.size):
    zmp = calculator.compute(
        np.array([
            com_x[i],
            com_y[i],
        ]),
        np.array([
            com_ddx[i],
            com_ddy[i],
        ]),
    )

    zmp_history.append(zmp)

zmp_history = np.asarray(
    zmp_history
)

support_x = (-0.08, 0.08)
support_y = (-0.04, 0.04)

plt.figure()

plt.plot(
    zmp_history[:, 0],
    zmp_history[:, 1],
    label="ZMP Path",
)

rectangle_x = [
    support_x[0],
    support_x[1],
    support_x[1],
    support_x[0],
    support_x[0],
]

rectangle_y = [
    support_y[0],
    support_y[0],
    support_y[1],
    support_y[1],
    support_y[0],
]

plt.plot(
    rectangle_x,
    rectangle_y,
    label="Support Polygon",
)

plt.axis("equal")
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title("Zero Moment Point")
plt.grid()
plt.legend()

plt.show()
