#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : SMO
@ Description        : smo 算法
@ Author             : XCrane
"""

import math

class SuperTwistingObserver:
    def __init__(
        self,
        k1=5.0,
        k2=20.0,
        dt=0.01,
        initial_position=0.0,
        initial_velocity=0.0,
    ):
        self.k1 = k1
        self.k2 = k2
        self.dt = dt
        self.position_estimate = initial_position
        self.velocity_estimate = initial_velocity

    @staticmethod
    def _sign(value):
        if value > 0:
            return 1.0
        if value < 0:
            return -1.0
        return 0.0

    def reset(
        self,
        position=0.0,
        velocity=0.0,
    ):
        self.position_estimate = position
        self.velocity_estimate = velocity

    def update(self, measurement, dt=None):
        if dt is None:
            dt = self.dt

        if dt <= 0:
            raise ValueError("dt must be greater than 0")

        error = measurement - self.position_estimate
        error_sign = self._sign(error)

        position_correction = (
            self.k1
            * math.sqrt(abs(error))
            * error_sign
        )

        self.position_estimate += dt * (
            self.velocity_estimate
            + position_correction
        )

        self.velocity_estimate += dt * (
            self.k2
            * error_sign
        )

        return (
            self.position_estimate,
            self.velocity_estimate,
        )
    