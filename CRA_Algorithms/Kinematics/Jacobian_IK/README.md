# Jacobian IK 雅可比数值逆运动学

## 1. 简介

Jacobian IK 是一种基于 Jacobian（雅可比矩阵）的数值逆运动学方法。

它不需要为机器人推导完整解析逆解，而是通过不断计算：

- 当前末端位置
- 当前末端误差
- 当前 Jacobian

逐步修正关节角，使末端执行器逼近目标位置。

本项目使用 **Damped Least Squares，阻尼最小二乘法**，相比直接使用 Jacobian 逆矩阵，在接近奇异位置时更加稳定。

---

## 2. 正运动学

二维二连杆机械臂末端位置为：

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

写成：

```math
\mathbf{x}
=
f(\mathbf{q})
```

其中：

```math
\mathbf{q}
=
\begin{bmatrix}
q_1 \\
q_2
\end{bmatrix}
```

---

## 3. 微分运动学

对末端位置进行微分：

```math
\dot{\mathbf{x}}
=
J(\mathbf{q})
\dot{\mathbf{q}}
```

其中：

```math
J(\mathbf{q})
=
\frac{
\partial \mathbf{x}
}{
\partial \mathbf{q}
}
```

就是 Jacobian 矩阵。

它描述：

> 关节的微小变化，会在末端产生怎样的运动变化。

---

## 4. 二连杆 Jacobian

对于二维二连杆：

```math
J
=
\begin{bmatrix}
\frac{\partial x}{\partial q_1}
&
\frac{\partial x}{\partial q_2}
\\
\frac{\partial y}{\partial q_1}
&
\frac{\partial y}{\partial q_2}
\end{bmatrix}
```

计算得到：

```math
J
=
\begin{bmatrix}
-l_1\sin q_1
-l_2\sin(q_1+q_2)
&
-l_2\sin(q_1+q_2)
\\
l_1\cos q_1
+l_2\cos(q_1+q_2)
&
l_2\cos(q_1+q_2)
\end{bmatrix}
```

---

## 5. 末端误差

目标位置为：

```math
\mathbf{x}_d
```

当前位置为：

```math
\mathbf{x}
```

则误差为：

```math
\mathbf{e}
=
\mathbf{x}_d
-
\mathbf{x}
```

希望通过改变关节角：

```math
\Delta\mathbf{q}
```

使末端位置向目标移动。

---

## 6. Jacobian 逆法

最直接的想法是：

```math
\Delta\mathbf{x}
=
J
\Delta\mathbf{q}
```

如果 $J$ 可逆：

```math
\Delta\mathbf{q}
=
J^{-1}
\Delta\mathbf{x}
```

因此可以使用：

```math
\Delta\mathbf{q}
=
J^{-1}
\mathbf{e}
```

不断更新关节角。

但是机器人在某些姿态下会出现 Jacobian 奇异或接近奇异，此时直接求逆会非常不稳定。

---

## 7. Jacobian 伪逆

对于非方阵或不可逆 Jacobian，可以使用 Moore-Penrose 伪逆：

```math
\Delta\mathbf{q}
=
J^{+}
\mathbf{e}
```

其中：

```math
J^{+}
```

表示 Jacobian 的伪逆。

但在接近奇异点时，伪逆仍可能产生很大的关节变化量。

---

## 8. Damped Least Squares

本项目采用阻尼最小二乘法：

```math
\Delta\mathbf{q}
=
J^T
\left(
JJ^T
+
\lambda^2I
\right)^{-1}
\mathbf{e}
```

其中：

- $\lambda$：阻尼系数
- $I$：单位矩阵
- $\mathbf{e}$：末端位置误差

当 Jacobian 接近奇异时：

```math
\lambda^2I
```

能够提高数值稳定性。

---

## 9. 迭代更新

得到：

```math
\Delta\mathbf{q}
```

以后，更新关节角：

```math
\mathbf{q}_{k+1}
=
\mathbf{q}_k
+
\alpha
\Delta\mathbf{q}_k
```

其中：

```math
\alpha
```

是步长。

程序中对应：

```python
q += self.step_size * delta_q
```

---

## 10. 收敛条件

每次迭代计算误差：

```math
\mathbf{e}_k
=
\mathbf{x}_d
-
\mathbf{x}_k
```

当：

```math
\left\|
\mathbf{e}_k
\right\|
<
\varepsilon
```

认为算法已经收敛。

其中：

```math
\varepsilon
```

对应程序中的：

```python
tolerance
```

---
