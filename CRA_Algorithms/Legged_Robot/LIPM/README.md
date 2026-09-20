# LIPM 线性倒立摆模型

## 1. 简介

LIPM，全称 **Linear Inverted Pendulum Model**，中文通常称为**线性倒立摆模型**。

它是双足机器人、类人机器人和腿式机器人中最经典的简化动力学模型之一。

LIPM 将复杂的人形机器人简化为：

- 一个集中质量点
- 一个固定高度的质心
- 一个位于地面的支撑点
- 忽略腿部质量和复杂关节动力学

这种简化使很多步态规划和平衡控制问题可以转化为较简单的线性系统。

常见应用包括：

- 双足机器人行走规划
- 质心轨迹规划
- ZMP 规划
- Capture Point
- 步点规划
- 平衡控制
- 人形机器人步态生成

---

## 2. 模型假设

LIPM 通常采用以下假设：

1. 机器人总质量集中在质心
2. 质心高度保持不变
3. 支撑脚与地面接触稳定
4. 垂直方向加速度忽略
5. 主要研究水平方向上的质心运动

设质心高度为：

```math
z_c
```

水平方向质心位置为：

```math
x
```

地面支撑点位置为：

```math
p
```

重力加速度为：

```math
g
```

---

## 3. LIPM 动力学方程

在线性倒立摆模型中：

```math
\ddot{x}
=
\frac{g}{z_c}
(x-p)
```

定义：

```math
\omega
=
\sqrt{
\frac{g}{z_c}
}
```

则可以写为：

```math
\ddot{x}
=
\omega^2
(x-p)
```

其中：

- $x$：质心水平位置
- $\ddot{x}$：质心水平加速度
- $p$：支撑点
- $z_c$：质心高度
- $\omega$：系统自然频率参数

---

## 4. 为什么是倒立摆

普通摆的质量位于支点下方，具有自然稳定性。

倒立摆的质量位于支点上方，稍微偏离平衡位置后就会继续向外倾倒。

例如当：

```math
x>p
```

则：

```math
x-p>0
```

因此：

```math
\ddot{x}>0
```

质心会继续向正方向加速。

这说明倒立摆本身是一个不稳定系统。

---

## 5. 状态空间形式

定义状态：

```math
\mathbf{x}
=
\begin{bmatrix}
x \\
\dot{x}
\end{bmatrix}
```

当支撑点固定在原点：

```math
p=0
```

可以写成：

```math
\dot{\mathbf{x}}
=
\begin{bmatrix}
0 & 1 \\
\omega^2 & 0
\end{bmatrix}
\mathbf{x}
```

如果考虑支撑点输入：

```math
\ddot{x}
=
\omega^2x
-
\omega^2p
```

则 $p$ 可以被看作系统控制输入。

---

## 6. Capture Point

Capture Point 是腿式机器人平衡控制中的重要概念。

对于 LIPM：

```math
\xi
=
x
+
\frac{\dot{x}}{\omega}
```

其中：

- $x$：当前质心位置
- $\dot{x}$：当前质心速度
- $\xi$：Capture Point

可以直观理解为：

> 如果机器人希望停止继续倾倒，需要把支撑点移动到哪里。

因此 Capture Point 常用于：

- 落脚点规划
- 推搡恢复
- 动态平衡
- 双足机器人行走控制

---

## 7. 创建模型

```python
model = LinearInvertedPendulum(
    com_height=0.8,
)
```

参数：

| 参数 | 含义 |
|---|---|
| `com_height` | 质心高度 $z_c$ |
| `gravity` | 重力加速度 $g$ |

模型内部计算：

```math
\omega
=
\sqrt{
\frac{g}{z_c}
}
```

---

## 8. 计算加速度

调用：

```python
acceleration = model.acceleration(
    position,
    support_point,
)
```

对应：

```math
\ddot{x}
=
\omega^2(x-p)
```

---

## 9. 离散仿真

程序使用简单数值积分：

```math
\dot{x}_{k+1}
=
\dot{x}_k
+
\ddot{x}_k
\Delta t
```

```math
x_{k+1}
=
x_k
+
\dot{x}_{k+1}
\Delta t
```

因此可以逐步模拟质心状态变化。

---

## 10. LIPM 的意义

真实双足机器人通常具有：

- 多自由度关节
- 腿部质量
- 复杂接触
- 非线性动力学
- 柔性与摩擦

直接使用完整动力学进行步态规划非常复杂。

LIPM 通过牺牲部分精度，将系统简化为：

```math
\ddot{x}
=
\omega^2(x-p)
```

从而能够快速进行：

- 步态规划
- 支撑点规划
- 平衡分析
- Capture Point 推导

---
