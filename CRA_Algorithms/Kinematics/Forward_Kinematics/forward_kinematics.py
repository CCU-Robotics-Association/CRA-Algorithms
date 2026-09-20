#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Forward-Kinematics
@ Description        : Forward Kinematics 算法
@ Author             : XCrane
"""

import numpy as np

class TwoLinkForwardKinematics:
    def __init__(
        self,
        l1=1.0,
        l2=0.7,
    ):
        self.l1 = l1
        self.l2 = l2

    def joint_positions(self, q):
        q1, q2 = np.asarray(
            q,
            dtype=float,
        )

        joint_1 = np.array([
            0.0,
            0.0,
        ])

        joint_2 = np.array([
            self.l1 * np.cos(q1),
            self.l1 * np.sin(q1),
        ])

        end_effector = joint_2 + np.array([
            self.l2 * np.cos(q1 + q2),
            self.l2 * np.sin(q1 + q2),
        ])

        return (
            joint_1,
            joint_2,
            end_effector,
        )

    def position(self, q):
        return self.joint_positions(q)[-1]

    def transform(self, q):
        q1, q2 = np.asarray(
            q,
            dtype=float,
        )

        theta = q1 + q2
        position = self.position(q)

        return np.array([
            [
                np.cos(theta),
                -np.sin(theta),
                position[0],
            ],
            [
                np.sin(theta),
                np.cos(theta),
                position[1],
            ],
            [
                0.0,
                0.0,
                1.0,
            ],
        ])
