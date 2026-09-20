#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Analytical-IK
@ Description        : Analytical Inverse Kinematics 算法
@ Author             : XCrane
"""

import numpy as np

class TwoLinkAnalyticalIK:
    def __init__(
        self,
        l1=1.0,
        l2=0.7,
    ):
        self.l1 = l1
        self.l2 = l2

    def solve(
        self,
        target,
        elbow="up",
    ):
        x, y = np.asarray(
            target,
            dtype=float,
        )

        r2 = x**2 + y**2

        cos_q2 = (
            r2
            - self.l1**2
            - self.l2**2
        ) / (
            2.0
            * self.l1
            * self.l2
        )

        tolerance = 1e-12

        if (
            cos_q2 < -1.0 - tolerance
            or cos_q2 > 1.0 + tolerance
        ):
            raise ValueError(
                "Target is outside the reachable workspace"
            )

        cos_q2 = np.clip(
            cos_q2,
            -1.0,
            1.0,
        )

        sin_q2_abs = np.sqrt(
            max(
                0.0,
                1.0 - cos_q2**2,
            )
        )

        if elbow == "up":
            sin_q2 = sin_q2_abs
        elif elbow == "down":
            sin_q2 = -sin_q2_abs
        else:
            raise ValueError(
                "elbow must be 'up' or 'down'"
            )

        q2 = np.arctan2(
            sin_q2,
            cos_q2,
        )

        q1 = (
            np.arctan2(y, x)
            - np.arctan2(
                self.l2 * sin_q2,
                self.l1
                + self.l2 * cos_q2,
            )
        )

        return np.array([
            q1,
            q2,
        ])
