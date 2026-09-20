# Forward Kinematics 正运动学

## 1. 简介

Forward Kinematics，中文通常称为**正运动学**或**前向运动学**。

它解决的问题是：

> 已知机器人的关节变量，末端执行器位于哪里、朝向哪里？

对于机械臂来说，输入通常是：

```math
\mathbf{q}
=
\begin{bmatrix}
q_1 \\
q_2 \\
\vdots \\
q_n
\end{bmatrix}
```

输出则是末端执行器的：

- 位置
- 姿态
- 齐次变换矩阵

正运动学是机器人运动学中最基础的问题之一。

---

## 2. 二连杆机械臂

本示例使用二维二连杆机械臂。

定义：

- 第一连杆长度为 $l_1$
- 第二连杆长度为 $l_2$
- 第一关节角为 $q_1$
- 第二关节角为 $q_2$

第二关节的位置为：

```math
x_1
=
l_1\cos q_1
```

```math
y_1
=
l_1\sin q_1
```

因此：

```math
\mathbf{p}_1
=
\begin{bmatrix}
l_1\cos q_1 \\
l_1\sin q_1
\end{bmatrix}
```

---

## 3. 末端位置

第二连杆相对于第一连杆的方向为：

```math
q_1+q_2
```

因此末端执行器位置为：

```math
x
=
l_1\cos q_1
+
l_2\cos(q_1+q_2)
```

```math
y
=
l_1\sin q_1
+
l_2\sin(q_1+q_2)
```

写成向量：

```math
\mathbf{p}
=
\begin{bmatrix}
x \\
y
\end{bmatrix}
```

这就是二维二连杆机械臂最基本的正运动学关系。

---

## 4. 末端姿态

在二维平面内，末端姿态可以使用一个角度表示：

```math
\theta
=
q_1+q_2
```

因此二维旋转矩阵为：

```math
R(\theta)
=
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
```

---

## 5. 齐次变换矩阵

将旋转和平移组合，可以得到二维齐次变换矩阵：

```math
T
=
\begin{bmatrix}
\cos\theta & -\sin\theta & x \\
\sin\theta & \cos\theta & y \\
0 & 0 & 1
\end{bmatrix}
```

其中：

```math
\theta
=
q_1+q_2
```

该矩阵同时描述了末端执行器的：

- 位置
- 姿态

---

## 6. 项目结构

```text
Forward_Kinematics/
├── forward_kinematics.py
├── demo.py
└── README.md
```

### `forward_kinematics.py`

实现二维二连杆机械臂正运动学。

主要接口：

```python
joint_positions()
```

返回：

- 基座位置
- 第二关节位置
- 末端位置

```python
position()
```

返回末端执行器二维位置。

```python
transform()
```

返回末端二维齐次变换矩阵。

---

## 7. 创建模型

```python
robot = TwoLinkForwardKinematics(
    l1=1.0,
    l2=0.7,
)
```

参数：

| 参数 | 含义 |
|---|---|
| `l1` | 第一连杆长度 |
| `l2` | 第二连杆长度 |

---

## 8. 计算末端位置

例如：

```python
q = np.array([
    0.5,
    0.3,
])

position = robot.position(q)
```

其数学过程为：

```math
\mathbf{q}
\longrightarrow
\mathbf{p}
```

也就是：

```math
(q_1,q_2)
\longrightarrow
(x,y)
```

---
