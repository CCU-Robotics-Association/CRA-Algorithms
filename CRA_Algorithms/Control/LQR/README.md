# LQR 线性二次型调节器

## 1. 简介

LQR（**Linear Quadratic Regulator**），即**线性二次型调节器**。

LQR 是现代控制理论中非常经典的一种最优状态反馈控制方法。

与 PID 主要根据系统误差进行控制不同，LQR 建立在线性状态空间模型之上，通过综合考虑：

* 系统状态偏差
* 控制输入大小

寻找一个最优状态反馈增益矩阵。

LQR 常用于：

* 倒立摆
* 两轮平衡机器人
* 无人机姿态控制
* 移动机器人轨迹跟踪
* 自动驾驶车辆横向控制
* 机械臂控制
* 四旋翼位置控制
* 足式机器人局部控制

---

## 2. 状态空间模型

LQR 通常针对连续时间线性系统：

```math
\dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u}
```

其中：

* $\mathbf{x}$：系统状态向量
* $\dot{\mathbf{x}}$：状态变化率
* $\mathbf{u}$：控制输入
* $A$：系统矩阵
* $B$：控制输入矩阵

例如一个移动物体可以使用：

```math
\mathbf{x}
=
\begin{bmatrix}
p\\
v
\end{bmatrix}
```

其中：

* $p$：位置
* $v$：速度

---

## 3. 状态反馈控制

LQR 使用状态反馈控制律：

```math
\mathbf{u}=-K\mathbf{x}
```

其中：

* $K$：状态反馈增益矩阵
* $\mathbf{x}$：当前状态
* $\mathbf{u}$：控制输入

因此 LQR 的核心任务就是寻找一个合适的：

```math
K
```

使系统稳定，并且具有较好的控制性能。

---

## 4. 关于负号

控制律为：

```math
\mathbf{u}=-K\mathbf{x}
```

前面的负号表示一种**负反馈**。

例如当前机器人位置为：

```math
p>0
```

而目标位置为：

```math
p_d=0
```

那么控制器应该产生一个向负方向的控制作用，使机器人向目标位置运动。

因此状态偏离目标的方向，与控制器修正方向相反。

---

## 5. LQR 的优化目标

LQR 不只是要求系统最终稳定。

它还希望同时解决两个问题：

### 问题一：状态误差应该尽可能小

即：

```math
\mathbf{x}\rightarrow0
```

### 问题二：控制输入不能无限大

实际执行器存在：

* 最大电压
* 最大电流
* 最大力矩
* 最大推力
* 最大速度

所以不能为了快速达到目标而产生无限大的控制输入。

因此 LQR 定义性能指标：

```math
J
=
\int_0^\infty
\left(
\mathbf{x}^TQ\mathbf{x}
+
\mathbf{u}^TR\mathbf{u}
\right)\,dt
```

LQR 的目标就是寻找：

```math
K
```

使：

```math
J
```

达到最小。

---

## 6. 状态权重矩阵 Q

代价函数中的：

```math
\mathbf{x}^TQ\mathbf{x}
```

用于衡量状态偏离目标的程度。

$Q$ 越大，意味着越重视状态误差。

例如：

```python
Q = np.array([
    [10.0, 0.0],
    [0.0, 1.0],
])
```

对应：

```math
Q
=
\begin{bmatrix}
10 & 0\\
0 & 1
\end{bmatrix}
```

如果状态为：

```math
\mathbf{x}
=
\begin{bmatrix}
p\\
v
\end{bmatrix}
```

则：

```math
\mathbf{x}^TQ\mathbf{x}=10p^2+v^2
```

因此这里对位置误差的惩罚是速度误差的 10 倍。

也就是说：

> 控制器更加重视位置能否快速回到目标。

---

## 7. 控制权重矩阵 R

代价函数中的：

```math
\mathbf{u}^TR\mathbf{u}
```

用于衡量控制输入的大小。

例如：

```python
R = np.array([
    [1.0],
])
```

即：

```math
R=
\begin{bmatrix}
1
\end{bmatrix}
```

如果增大 $R$：

```math
R\uparrow
```

意味着：

> 使用控制输入的代价变高。

因此控制器通常会变得更加温和。

如果减小 $R$：

```math
R\downarrow
```

意味着：

> 控制器允许使用更大的控制输入。

因此控制通常会更加激进。

---

## 8. Q 与 R 的直观理解

可以把 LQR 看成在两个目标之间寻找平衡：

```text
尽快让系统回到目标
          ↕
尽量不要使用过大的控制输入
```

$Q$ 决定：

> 有多在意状态误差。

$R$ 决定：

> 有多在意控制成本。

因此：

```text
Q 增大
    ↓
更重视状态误差
    ↓
控制通常更积极
```

而：

```text
R 增大
    ↓
更重视控制成本
    ↓
控制通常更温和
```

---

## 9. Riccati 方程

为了获得最优反馈增益 $K$，LQR 需要求解连续时间代数 Riccati 方程：

```math
A^TP
+
PA
-
PBR^{-1}B^TP
+
Q
=
0
```

其中：

```math
P
```

是需要求解的对称矩阵。

得到 $P$ 后，可以计算最优反馈增益：

```math
K=R^{-1}B^TP
```

最终得到控制律：

```math
\mathbf{u}=-K\mathbf{x}
```

---

## 10. 程序中的 Riccati 方程求解

本项目使用 SciPy：

```python
solve_continuous_are(
    A,
    B,
    Q,
    R,
)
```

求解连续时间代数 Riccati 方程。

得到：

```python
P
```

随后计算：

```python
K = np.linalg.solve(
    R,
    B.T @ P,
)
```

理论公式是：

```math
K=R^{-1}B^TP
```

代码中没有直接使用：

```python
np.linalg.inv(R)
```

而使用：

```python
np.linalg.solve()
```

求解线性方程。

在数值计算中，这通常比直接求逆矩阵具有更好的数值稳定性。

---

## 11. 闭环系统

原系统为：

```math
\dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u}
```

LQR 控制律为：

```math
\mathbf{u}=-K\mathbf{x}
```

将 LQR 控制律代入原系统：

```math
\dot{\mathbf{x}}=A\mathbf{x}+B(-K\mathbf{x})
```

整理可得：

```math
\dot{\mathbf{x}}=A\mathbf{x}-BK\mathbf{x}
```

进一步得到：

```math
\dot{\mathbf{x}}=(A-BK)\mathbf{x}
```

因此，LQR 控制后的闭环系统矩阵为：

```math
A_{\mathrm{cl}}=A-BK
```

## 12. 闭环特征值

程序计算：

```python
eigenvalues = np.linalg.eigvals(
    closed_loop_matrix
)
```

即求：

```math
A-BK
```

的特征值。

对于连续时间线性系统，如果所有闭环特征值均满足：

```math
\operatorname{Re}(\lambda_i)<0
```

则闭环系统通常是渐近稳定的。

也就是说：

```math
\mathbf{x}(t)\rightarrow0
```

当：

```math
t\rightarrow\infty
```

---

## 13. Demo 

本 Demo 使用经典的 **Double Integrator（二重积分器）** 模型。

假设一个物体在一维空间运动。

状态定义为：

```math
\mathbf{x}
=
\begin{bmatrix}
p\\
v
\end{bmatrix}
```

其中：

* $p$：位置
* $v$：速度

控制输入：

```math
u
```

表示加速度。

系统满足：

```math
\dot{p}=v
```

以及：

```math
\dot{v}=u
```

写成矩阵：

```math
\begin{bmatrix}
\dot{p}\\
\dot{v}
\end{bmatrix}
=
\begin{bmatrix}
0 & 1\\
0 & 0
\end{bmatrix}
\begin{bmatrix}
p\\
v
\end{bmatrix}
+
\begin{bmatrix}
0\\
1
\end{bmatrix}u
```

因此：

```math
A
=
\begin{bmatrix}
0 & 1\\
0 & 0
\end{bmatrix}
```

以及：

```math
B
=
\begin{bmatrix}
0\\
1
\end{bmatrix}
```

代码中：

```python
A = np.array([
    [0.0, 1.0],
    [0.0, 0.0],
])

B = np.array([
    [0.0],
    [1.0],
])
```

---

由：

```math
\dot{v}=u
```

对时间积分一次：

```math
v(t)=\int u(t)\,dt
```

又因为：

```math
\dot{p}=v
```

再次积分：

```math
p(t)=\int v(t)\,dt
```

因此控制输入 $u$ 经过两次积分才能影响位置 $p$。

所以称为：

> Double Integrator

即二重积分器。

---

## 14. 仿真初始条件

Demo 设置：

```math
\mathbf{x}(0)
=
\begin{bmatrix}
5\\
0
\end{bmatrix}
```

表示：

```math
p(0)=5
```

```math
v(0)=0
```

也就是机器人一开始：

```text
位置 = 5
速度 = 0
```

目标状态为：

```math
\mathbf{x}_d
=
\begin{bmatrix}
0\\
0
\end{bmatrix}
```

即：

```text
位置 = 0
速度 = 0
```

---

## 15. LQR 控制过程

每一个控制周期都执行：

```math
\mathbf{u}_k=-K\mathbf{x}_k
```

然后根据：

```math
\dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u}
```

计算系统状态变化率。

整个过程可以理解为：

```text
当前状态 x
    ↓
LQR
    ↓
u = -Kx
    ↓
被控系统
    ↓
产生新的状态
    ↓
重新反馈给 LQR
```

---

## 16. 欧拉积分

由于状态空间方程是连续时间形式：

```math
\dot{\mathbf{x}}=A\mathbf{x}+B\mathbf{u}
```

仿真程序需要将其离散计算。

本项目使用 Euler 欧拉积分：

```math
\mathbf{x}_{k+1}=\mathbf{x}_k+\dot{\mathbf{x}}_k\Delta t
```

其中：

```math
\dot{\mathbf{x}}_k=A\mathbf{x}_k+B\mathbf{u}_k
```

因此：

```math
\mathbf{x}_{k+1}
=
\mathbf{x}_k
+
\left(
A\mathbf{x}_k
+
B\mathbf{u}_k
\right)\Delta t
```

对应代码：

```python
state_dot = (
    A @ state
    +
    B @ u
)

state += state_dot * dt
```

---

## 17. LQR 函数

调用：

```python
K, P, eigenvalues = lqr(
    A,
    B,
    Q,
    R,
)
```

输入：

| 参数  | 含义     |
| --- | ------ |
| `A` | 状态矩阵   |
| `B` | 输入矩阵   |
| `Q` | 状态权重矩阵 |
| `R` | 控制权重矩阵 |

返回：

| 参数            | 含义          |
| ------------- | ----------- |
| `K`           | 最优状态反馈增益    |
| `P`           | Riccati 方程解 |
| `eigenvalues` | 闭环系统特征值     |

---

## 18. LQR 调参

LQR 通常不直接手动修改：

```math
K
```

而是调节：

```math
Q
```

和：

```math
R
```

再自动求解：

```math
K
```

---

### 增大位置权重

例如从：

```math
Q
=
\begin{bmatrix}
10 & 0\\
0 & 1
\end{bmatrix}
```

改为：

```math
Q
=
\begin{bmatrix}
100 & 0\\
0 & 1
\end{bmatrix}
```

意味着：

> 更加不能接受位置偏差。

控制器通常会更加积极地让位置回到目标。

---

### 增大速度权重

例如：

```math
Q
=
\begin{bmatrix}
10 & 0\\
0 & 20
\end{bmatrix}
```

意味着：

> 更加重视速度不能过大。

因此系统运动可能更加平稳。

---

### 增大 R

例如：

```math
R=10
```

意味着：

> 控制输入的代价更高。

因此：

```math
\lvert u\rvert
```

通常会减小。

但系统回到目标的速度也可能变慢。

---

## 19. PID 与 LQR 的区别

| PID               | LQR          |
| ----------------- | ------------ |
| 基于误差反馈            | 基于状态反馈       |
| 通常不需要精确模型         | 需要状态空间模型     |
| 参数为 $K_p,K_i,K_d$ | 参数主要为 $Q,R$  |
| 调参具有较强经验性         | 基于最优控制理论     |
| 算法简单              | 数学基础更完整      |
| 工业控制非常常见          | 机器人和现代控制非常常见 |
| 单输入单输出使用方便        | 多变量系统优势明显    |

---
