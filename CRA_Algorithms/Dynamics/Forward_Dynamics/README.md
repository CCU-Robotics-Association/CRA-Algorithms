# Forward Dynamics 正向动力学

## 1. 简介

Forward Dynamics，中文通常称为**正向动力学**或**前向动力学**。

它解决的问题与逆动力学相反。

逆动力学的问题是：

> 已知位置、速度和加速度，需要多大的关节力矩？

即：

```math
(
\mathbf{q},
\dot{\mathbf{q}},
\ddot{\mathbf{q}}
)
\longrightarrow
\boldsymbol{\tau}
```

正向动力学的问题是：

> 已知机器人当前状态和施加的关节力矩，机器人会产生多大的关节加速度？

即：

```math
(
\mathbf{q},
\dot{\mathbf{q}},
\boldsymbol{\tau}
)
\longrightarrow
\ddot{\mathbf{q}}
```

正向动力学是机器人仿真的基础。

---

## 2. 标准动力学方程

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
- $\mathbf{c}(\mathbf{q},\dot{\mathbf{q}})$：科氏力与离心力
- $\mathbf{g}(\mathbf{q})$：重力项
- $\boldsymbol{\tau}$：关节力矩
- $\ddot{\mathbf{q}}$：关节加速度

---

## 3. 求解关节加速度

将科氏力和重力移到等式右侧：

```math
M(\mathbf{q})
\ddot{\mathbf{q}}
=
\boldsymbol{\tau}
-
\mathbf{c}(
\mathbf{q},
\dot{\mathbf{q}}
)
-
\mathbf{g}(\mathbf{q})
```

理论上可以写成：

```math
\ddot{\mathbf{q}}
=
M^{-1}(\mathbf{q})
\left[
\boldsymbol{\tau}
-
\mathbf{c}(
\mathbf{q},
\dot{\mathbf{q}}
)
-
\mathbf{g}(\mathbf{q})
\right]
```

但实际数值计算中，一般不建议显式计算：

```math
M^{-1}
```

而是直接求解线性方程：

```math
M(\mathbf{q})
\ddot{\mathbf{q}}
=
\mathbf{b}
```

其中：

```math
\mathbf{b}
=
\boldsymbol{\tau}
-
\mathbf{c}
-
\mathbf{g}
```

因此代码使用：

```python
np.linalg.solve()
```

而不是：

```python
np.linalg.inv()
```

---

## 4. 为什么不直接求逆矩阵

理论公式中经常出现：

```math
M^{-1}
```

但计算机进行数值计算时，显式求矩阵逆通常：

- 计算量更大
- 数值稳定性较差
- 没有必要

因此更合理的方式是直接求解：

```math
M\mathbf{x}
=
\mathbf{b}
```

得到：

```math
\mathbf{x}
=
\ddot{\mathbf{q}}
```

这也是很多机器人动力学库采用的基本思想。

---

## 5. 质量矩阵

二连杆机器人质量矩阵为：

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
m_1c_1^2
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

可以看到：

```math
M(\mathbf{q})
```

会随机器人构型变化。

这意味着同样的关节力矩，在不同姿态下可能产生不同的关节加速度。

---

## 6. 科氏力与离心力

本示例使用：

```math
h
=
-m_2l_1c_2\sin q_2
```

以及：

```math
\mathbf{c}
=
\begin{bmatrix}
h
(
2\dot{q}_1\dot{q}_2
+
\dot{q}_2^2
)
\\
-h\dot{q}_1^2
\end{bmatrix}
```

当机器人高速运动时，这部分可能对系统行为产生明显影响。

---

## 7. 重力项

重力向量为：

```math
\mathbf{g}
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
gm_2c_2\cos(q_1+q_2)
```

因此即使：

```math
\boldsymbol{\tau}
=
0
```

机器人也可能因为重力产生加速度。

---

## 8. 正向动力学函数

本项目核心调用为：

```python
ddq = model.acceleration(
    q,
    dq,
    tau,
)
```

输入：

- `q`：关节位置
- `dq`：关节速度
- `tau`：关节力矩

输出：

- `ddq`：关节加速度

其数学意义为：

```math
\ddot{\mathbf{q}}
=
\mathrm{ForwardDynamics}
(
\mathbf{q},
\dot{\mathbf{q}},
\boldsymbol{\tau}
)
```

---

## 9. 为什么不同姿态下加速度不同

因为质量矩阵：

```math
M(\mathbf{q})
```

与机器人构型有关。

特别是二连杆系统中存在：

```math
\cos q_2
```

因此当第二关节角改变时：

```math
M(\mathbf{q})
```

也会发生改变。

同时重力项：

```math
\mathbf{g}(\mathbf{q})
```

也会随着姿态改变。

所以即使施加完全相同的：

```math
\boldsymbol{\tau}
```

机器人产生的：

```math
\ddot{\mathbf{q}}
```

仍然可能明显不同。

这正是机器人动力学非线性和耦合性的一个直观表现。

---

## 10. 正向动力学与仿真

机器人仿真一般不断重复以下过程：

```text
当前 q、dq
    ↓
施加 tau
    ↓
Forward Dynamics
    ↓
得到 ddq
    ↓
数值积分
    ↓
得到新的 dq
    ↓
再次积分
    ↓
得到新的 q
```

数学上：

```math
\dot{\mathbf{q}}_{k+1}
=
\dot{\mathbf{q}}_k
+
\ddot{\mathbf{q}}_k
\Delta t
```

```math
\mathbf{q}_{k+1}
=
\mathbf{q}_k
+
\dot{\mathbf{q}}_{k+1}
\Delta t
```

MuJoCo、PyBullet、Gazebo 等物理仿真系统本质上都需要解决类似的动力学推进问题，只是实际实现还会进一步考虑接触、碰撞、约束和数值积分等问题。

---

## 11. 与逆动力学的区别

| 正向动力学 | 逆动力学 |
|---|---|
| 已知 $\boldsymbol{\tau}$ | 已知 $\ddot{\mathbf{q}}$ |
| 求 $\ddot{\mathbf{q}}$ | 求 $\boldsymbol{\tau}$ |
| 常用于物理仿真 | 常用于控制 |
| 预测机器人怎么运动 | 计算如何让机器人运动 |

正向动力学：

```math
(
\mathbf{q},
\dot{\mathbf{q}},
\boldsymbol{\tau}
)
\rightarrow
\ddot{\mathbf{q}}
```

逆动力学：

```math
(
\mathbf{q},
\dot{\mathbf{q}},
\ddot{\mathbf{q}}
)
\rightarrow
\boldsymbol{\tau}
```

---
