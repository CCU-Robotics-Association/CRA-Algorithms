#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Raibert-Controller
@ Description        : Raibert Foot Placement 算法
@ Author             : XCrane
"""

import numpy as np

class RaibertFootPlacement:
    def __init__(
        self,
        stance_time=0.25,
        velocity_gain=0.15,
    ):
        self.stance_time = stance_time
        self.velocity_gain = velocity_gain

    def compute(
        self,
        current_velocity,
        desired_velocity,
    ):
        current_velocity = np.asarray(
            current_velocity,
            dtype=float,
        )

        desired_velocity = np.asarray(
            desired_velocity,
            dtype=float,
        )

        nominal_step = (
            0.5
            * self.stance_time
            * current_velocity
        )

        velocity_correction = (
            self.velocity_gain
            * (
                current_velocity
                - desired_velocity
            )
        )

        return (
            nominal_step
            + velocity_correction
        )
