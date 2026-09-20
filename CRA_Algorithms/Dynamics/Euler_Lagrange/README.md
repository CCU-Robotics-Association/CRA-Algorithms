# Euler-Lagrange 动力学

## 1. 简介

Euler-Lagrange 方法是机器人动力学中最经典的建模方法之一。

它从系统的动能与势能出发，通过 Lagrange 方程建立关节位置、速度、加速度与驱动力矩之间的关系。

在机器人领域，它常用于：

- 机械臂动力学建模
- 逆动力学计算
- 重力补偿
- 计算力矩控制
- 模型预测控制
- 仿真模型建立
- 参数辨识

以二维二连杆机械臂为例。

---

## 2. 广义坐标

定义机械臂关节角：

```math
\mathbf{q}
=
\begin{bmatrix}
q_1 \\
q_2
\end{bmatrix}
```

关节角速度：

```math
\dot{\mathbf{q}}
=
\begin{bmatrix}
\dot{q}_1 \\
\dot{q}_2
\end{bmatrix}
```

关节角加速度：

```math
\ddot{\mathbf{q}}
=
\begin{bmatrix}
\ddot{q}_1 \\
\ddot{q}_2
\end{bmatrix}
```

关节驱动力矩：

```math
\boldsymbol{\tau}
=
\begin{bmatrix}
\tau_1 \\
\tau_2
\end{bmatrix}
```

---

## 3. Lagrangian

定义系统总动能为：

```math
T
```

总势能为：

```math
V
```

Lagrangian 定义为：

```math
L
=
T-V
```

对于第 $i$ 个广义坐标，Euler-Lagrange 方程为：

```math
\frac{d}{dt}
\left(
\frac{\partial L}{\partial \dot{q}_i}
\right)
-
\frac{\partial L}{\partial q_i}
=
\tau_i
```

对所有关节展开后，可以得到机器人的标准动力学方程。

---

## 4. 机器人标准动力学方程

机器人动力学通常写成：

```math
M(\mathbf{q})
\ddot{\mathbf{q}}
+
\mathbf{c}(
\mathbf{q},
\dot{\mathbf{q}}
)
+
\mathbf{g}(\mathbf{q})
=
\boldsymbol{\tau}
```

其中：

- $M(\mathbf{q})$：质量矩阵
- $\mathbf{c}(\mathbf{q},\dot{\mathbf{q}})$：科氏力与离心力项
- $\mathbf{g}(\mathbf{q})$：重力项
- $\boldsymbol{\tau}$：关节力矩

本项目中的 `inverse_dynamics()` 就是在计算该方程右侧所需要的关节力矩。

---

## 5. 质量矩阵

对于本项目中的二连杆机械臂：

```math
M(\mathbf{q})
=
\begin{bmatrix}
M_{11} & M_{12} \\
M_{12} & M_{22}
\end{bmatrix}
```

其中：

```math
M_{11}
=
I_1
+
I_2
+
m_1 c_1^2
+
m_2
\left(
l_1^2
+
c_2^2
+
2l_1c_2\cos q_2
\right)
```

```math
M_{12}
=
I_2
+
m_2
\left(
c_2^2
+
l_1c_2\cos q_2
\right)
```

```math
M_{22}
=
I_2
+
m_2c_2^2
```

其中：

- $m_1,m_2$：连杆质量
- $l_1,l_2$：连杆长度
- $c_1,c_2$：关节到质心的距离
- $I_1,I_2$：连杆绕质心的转动惯量

质量矩阵描述系统的惯性特性。

---

## 6. 科氏力与离心力

定义：

```math
h
=
-m_2l_1c_2\sin q_2
```

则本项目使用的科氏力与离心力向量为：

```math
\mathbf{c}
=
\begin{bmatrix}
h
\left(
2\dot{q}_1\dot{q}_2
+
\dot{q}_2^2
\right)
\\
-h\dot{q}_1^2
\end{bmatrix}
```

这部分反映多个关节同时运动时产生的动力学耦合。

当机器人运动速度增大时，这些项通常会更加明显。

---

## 7. 重力项

本项目假设关节角从水平轴开始测量。

重力向量为：

```math
\mathbf{g}(\mathbf{q})
=
\begin{bmatrix}
g_1 \\
g_2
\end{bmatrix}
```

其中：

```math
g_1
=
g
\left[
(m_1c_1+m_2l_1)\cos q_1
+
m_2c_2\cos(q_1+q_2)
\right]
```

```math
g_2
=
gm_2c_2
\cos(q_1+q_2)
```

如果机器人静止：

```math
\dot{\mathbf{q}}
=
0
```

且：

```math
\ddot{\mathbf{q}}
=
0
```

则保持当前姿态所需要的力矩就是：

```math
\boldsymbol{\tau}
=
\mathbf{g}(\mathbf{q})
```

这就是重力补偿的基本思想。

---

## 8. 逆动力学

逆动力学解决的问题是：

> 已知机器人希望达到的位置、速度和加速度，需要施加多大的关节力矩？

输入：

```math
\mathbf{q},
\quad
\dot{\mathbf{q}},
\quad
\ddot{\mathbf{q}}
```

输出：

```math
\boldsymbol{\tau}
```

计算公式为：

```math
\boldsymbol{\tau}
=
M(\mathbf{q})
\ddot{\mathbf{q}}
+
\mathbf{c}(
\mathbf{q},
\dot{\mathbf{q}}
)
+
\mathbf{g}(\mathbf{q})
```

---

## 9. 创建模型

```python
model = TwoLinkEulerLagrange()
```

默认参数：

| 参数 | 含义 |
|---|---|
| `m1` | 连杆 1 质量 |
| `m2` | 连杆 2 质量 |
| `l1` | 连杆 1 长度 |
| `l2` | 连杆 2 长度 |
| `c1` | 连杆 1 质心距离 |
| `c2` | 连杆 2 质心距离 |
| `i1` | 连杆 1 转动惯量 |
| `i2` | 连杆 2 转动惯量 |
| `gravity` | 重力加速度 |

---

## 10. 调用逆动力学

```python
tau = model.inverse_dynamics(
    q,
    dq,
    ddq,
)
```

其中：

- `q`：关节角
- `dq`：关节角速度
- `ddq`：关节角加速度
- `tau`：所需关节力矩

---
