#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : ZMP
@ Description        : ZMP 算法
@ Author             : XCrane
"""

import numpy as np

class ZMPCalculator:
    def __init__(
        self,
        com_height=0.8,
        gravity=9.81,
    ):
        self.com_height = com_height
        self.gravity = gravity

    def compute(
        self,
        com_position,
        com_acceleration,
    ):
        position = np.asarray(
            com_position,
            dtype=float,
        )

        acceleration = np.asarray(
            com_acceleration,
            dtype=float,
        )

        return (
            position
            - self.com_height
            / self.gravity
            * acceleration
        )

    @staticmethod
    def is_inside_support_polygon(
        zmp,
        x_limits,
        y_limits,
    ):
        x, y = np.asarray(
            zmp,
            dtype=float,
        )

        return (
            x_limits[0]
            <= x
            <= x_limits[1]
            and y_limits[0]
            <= y
            <= y_limits[1]
        )
