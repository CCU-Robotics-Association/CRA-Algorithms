#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : PID
@ Description        : pid 算法
@ Author             : XCrane
"""

class PID:

    def __init__(
        self,
        kp,
        ki,
        kd,
        dt=0.01,
        output_limits=(None, None),
        integral_limits=(None, None),
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.output_limits = output_limits
        self.integral_limits = integral_limits
        self.integral = 0.0
        self.previous_error = 0.0
        self.first_update = True

    @staticmethod
    def _clamp(value, limits):

        lower, upper = limits
        if lower is not None:
            value = max(lower, value)
        if upper is not None:
            value = min(upper, value)
        return value

    def reset(self):

        self.integral = 0.0
        self.previous_error = 0.0
        self.first_update = True

    def update(self, setpoint, measurement, dt=None):

        if dt is None:
            dt = self.dt
        if dt <= 0:
            raise ValueError(" dt <= 0")
        error = setpoint - measurement
        proportional_term = self.kp * error
        self.integral += error * dt
        self.integral = self._clamp(
            self.integral,
            self.integral_limits,
        )
        integral_term = self.ki * self.integral
        if self.first_update:
            derivative = 0.0
            self.first_update = False
        else:
            derivative = (
                error - self.previous_error
            ) / dt
        derivative_term = self.kd * derivative
        self.previous_error = error
        output = (
            proportional_term
            + integral_term
            + derivative_term
        )
        output = self._clamp(
            output,
            self.output_limits,
        )
        return output