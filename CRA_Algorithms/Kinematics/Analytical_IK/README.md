# Analytical IK 解析逆运动学

## 1. 简介

Inverse Kinematics，简称 IK，中文通常称为**逆运动学**。

它解决的问题是：

> 已知末端执行器希望到达的位置或姿态，机器人各个关节应该取什么值？

正运动学是：

```math
\mathbf{q}
\longrightarrow
\mathbf{x}
```

逆运动学则是：

```math
\mathbf{x}
\longrightarrow
\mathbf{q}
```

本项目实现二维二连杆机械臂的**解析逆运动学**。

解析法直接通过几何关系和三角函数求出关节角，不需要迭代优化。

---

## 2. 二连杆机械臂

机械臂参数：

- 第一连杆长度 $l_1$
- 第二连杆长度 $l_2$
- 第一关节角 $q_1$
- 第二关节角 $q_2$

目标末端位置为：

```math
\mathbf{p}
=
\begin{bmatrix}
x \\
y
\end{bmatrix}
```

目标点到基座的距离满足：

```math
r^2
=
x^2+y^2
```

---

## 3. 求第二关节角

根据余弦定理：

```math
r^2
=
l_1^2
+
l_2^2
+
2l_1l_2\cos q_2
```

因此：

```math
\cos q_2
=
\frac{
x^2+y^2-l_1^2-l_2^2
}{
2l_1l_2
}
```

为了获得完整角度，还需要：

```math
\sin q_2
=
\pm
\sqrt{
1-\cos^2 q_2
}
```

因此：

```math
q_2
=
\operatorname{atan2}
\left(
\sin q_2,
\cos q_2
\right)
```

正负号对应两种不同的机械臂构型。

---

## 4. Elbow Up 与 Elbow Down

二维二连杆机械臂到达同一个目标点时，通常存在两组关节解。

本项目称为：

- `elbow="up"`
- `elbow="down"`

对应：

```math
\sin q_2
=
+
\sqrt{
1-\cos^2 q_2
}
```

和：

```math
\sin q_2
=
-
\sqrt{
1-\cos^2 q_2
}
```

因此逆运动学并不一定只有唯一解。

---

## 5. 求第一关节角

首先定义目标方向角：

```math
\phi
=
\operatorname{atan2}(y,x)
```

再根据机械臂几何关系：

```math
q_1
=
\operatorname{atan2}(y,x)
-
\operatorname{atan2}
\left(
l_2\sin q_2,
l_1+l_2\cos q_2
\right)
```

这样即可得到第一关节角。

---

## 6. 可达工作空间

二连杆机械臂能够到达目标点的基本条件为：

```math
|l_1-l_2|
\leq
r
\leq
l_1+l_2
```

其中：

```math
r
=
\sqrt{x^2+y^2}
```

如果：

```math
r
>
l_1+l_2
```

目标点太远，机械臂无法到达。

如果：

```math
r
<
|l_1-l_2|
```

目标点位于机械臂内部不可达区域。

代码通过检查：

```math
\cos q_2
\in
[-1,1]
```

判断目标是否可达。

---

## 7. 创建求解器

```python
solver = TwoLinkAnalyticalIK(
    l1=1.0,
    l2=0.7,
)
```

---

## 8. 求解逆运动学

目标位置：

```python
target = np.array([
    1.0,
    0.8,
])
```

肘部向上：

```python
q = solver.solve(
    target,
    elbow="up",
)
```

肘部向下：

```python
q = solver.solve(
    target,
    elbow="down",
)
```

输出：

```math
\mathbf{q}
=
\begin{bmatrix}
q_1 \\
q_2
\end{bmatrix}
```

---
