<!--
作者 / Author: XCrane
-->

<div align="center">

<a href="https://github.com/CCU-Robotics-Association">
  <img src="https://raw.githubusercontent.com/CCU-Robotics-Association/.github/main/profile/assets/logo.svg" width="132" alt="CCU Robotics Association Logo">
</a>

# CCU Robotics Association

### 机器人算法资料 · Robotics Algorithms

CCU 机器人协会 · 2024 —— Future

[![Organization](./assets/cra-association-badge.svg)](https://github.com/CCU-Robotics-Association)
![Python](./assets/python-badge.svg)
![NumPy](./assets/numpy-badge.svg)

[**官网(Website) »**](https://ccu-robotics-association.github.io/) | [**GitHub 主页 »**](https://github.com/CCU-Robotics-Association) | [**算法仓库(Algorithms) »**](https://github.com/CCU-Robotics-Association/CRA-Algorithms)

> **一  同  奋  进  前  行  ，  共  就  非  凡  之  事**

</div>

---

## <img src="./assets/icons/book-open.svg" width="22" height="22" alt=""> Overview | 内容介绍

本目录整理 ***CRA*** 的机器人算法资料，覆盖控制、运动学、动力学、腿式机器人、碰撞检测与计算机视觉

每个模块包含算法说明、Python 实现与演示脚本，便于结合原理、代码和可视化结果学习

[控制](#control) · [运动学](#kinematics) · [动力学](#dynamics) · [腿式机器人](#legged-robot) · [碰撞检测](#collision-detection) · [计算机视觉](#computer-vision) · [快速开始](#quick-start)

## <img src="./assets/icons/users-round.svg" width="22" height="22" alt=""> Author | 编写作者

XCrane

<a name="algorithms"></a>

## <img src="./assets/icons/folder-open.svg" width="22" height="22" alt=""> Algorithms | 算法索引

<a name="control"></a>

### Control | 控制

| 算法 | 主要内容 | 资料与示例 |
| :--- | :--- | :--- |
| **PID** | 比例、积分、微分反馈与输出限幅 | [说明](./Control/PID/README.md) · [实现](./Control/PID/pid.py) · [演示](./Control/PID/demo.py) |
| **LQR** | 连续时间线性二次型调节器与状态反馈 | [说明](./Control/LQR/README.md) · [实现](./Control/LQR/lqr.py) · [演示](./Control/LQR/demo.py) |
| **SMO** | Super-Twisting 滑模观测器，估计位置与速度 | [说明](./Control/SMO/README.md) · [实现](./Control/SMO/smo.py) · [演示](./Control/SMO/demo.py) |

<a name="kinematics"></a>

### Kinematics | 运动学

| 算法 | 主要内容 | 资料与示例 |
| :--- | :--- | :--- |
| **Forward Kinematics** | 平面二连杆机械臂正运动学 | [说明](./Kinematics/Forward_Kinematics/README.md) · [实现](./Kinematics/Forward_Kinematics/forward_kinematics.py) · [演示](./Kinematics/Forward_Kinematics/demo.py) |
| **Analytical IK** | 平面二连杆机械臂解析逆运动学 | [说明](./Kinematics/Analytical_IK/README.md) · [实现](./Kinematics/Analytical_IK/analytical_ik.py) · [演示](./Kinematics/Analytical_IK/demo.py) |
| **Jacobian IK** | 基于阻尼最小二乘法的数值逆运动学 | [说明](./Kinematics/Jacobian_IK/README.md) · [实现](./Kinematics/Jacobian_IK/jacobian_ik.py) · [演示](./Kinematics/Jacobian_IK/demo.py) |

<a name="dynamics"></a>

### Dynamics | 动力学

| 算法 | 主要内容 | 资料与示例 |
| :--- | :--- | :--- |
| **Euler-Lagrange** | 由动能、势能建立二连杆动力学模型 | [说明](./Dynamics/Euler_Lagrange/README.md) · [实现](./Dynamics/Euler_Lagrange/euler_lagrange.py) · [演示](./Dynamics/Euler_Lagrange/demo.py) |
| **RNEA** | 递归牛顿-欧拉逆动力学，计算关节力矩 | [说明](./Dynamics/RNEA/README.md) · [实现](./Dynamics/RNEA/rnea.py) · [演示](./Dynamics/RNEA/demo.py) |
| **Forward Dynamics** | 根据关节状态与力矩计算加速度 | [说明](./Dynamics/Forward_Dynamics/README.md) · [实现](./Dynamics/Forward_Dynamics/forward_dynamics.py) · [演示](./Dynamics/Forward_Dynamics/demo.py) |

<a name="legged-robot"></a>

### Legged Robot | 腿式机器人

| 算法 | 主要内容 | 资料与示例 |
| :--- | :--- | :--- |
| **LIPM** | 线性倒立摆模型与质心运动 | [说明](./Legged_Robot/LIPM/README.md) · [实现](./Legged_Robot/LIPM/lipm.py) · [演示](./Legged_Robot/LIPM/demo.py) |
| **Raibert Controller** | 根据速度误差调节落脚点 | [说明](./Legged_Robot/Raibert_Controller/README.md) · [实现](./Legged_Robot/Raibert_Controller/raibert.py) · [演示](./Legged_Robot/Raibert_Controller/demo.py) |
| **ZMP** | 零力矩点计算与支撑区域分析 | [说明](./Legged_Robot/ZMP/README.md) · [实现](./Legged_Robot/ZMP/zmp.py) · [演示](./Legged_Robot/ZMP/demo.py) |

<a name="collision-detection"></a>

### Collision Detection | 碰撞检测

| 算法 | 主要内容 | 资料与示例 |
| :--- | :--- | :--- |
| **AABB** | 轴对齐包围盒重叠检测 | [说明](./Collision_Detection/AABB/README.md) · [实现](./Collision_Detection/AABB/aabb.py) · [演示](./Collision_Detection/AABB/demo.py) |
| **SAT** | 基于分离轴定理的二维凸多边形碰撞检测 | [说明](./Collision_Detection/SAT/README.md) · [实现](./Collision_Detection/SAT/sat.py) · [演示](./Collision_Detection/SAT/demo.py) |
| **GJK** | 基于支撑映射与 Minkowski 差的二维凸体碰撞检测 | [说明](./Collision_Detection/GJK/README.md) · [实现](./Collision_Detection/GJK/gjk.py) · [演示](./Collision_Detection/GJK/demo.py) |

<a name="computer-vision"></a>

### Computer Vision | 计算机视觉

| 算法 | 主要内容 | 资料与示例 |
| :--- | :--- | :--- |
| **Sobel** | 图像梯度与边缘检测 | [说明](./Computer_Vision/Sobel/README.md) · [实现](./Computer_Vision/Sobel/sobel.py) · [演示](./Computer_Vision/Sobel/demo.py) |
| **Harris** | 角点响应与局部特征点检测 | [说明](./Computer_Vision/Harris/README.md) · [实现](./Computer_Vision/Harris/harris.py) · [演示](./Computer_Vision/Harris/demo.py) |
| **HOG** | 方向梯度直方图特征提取 | [说明](./Computer_Vision/HOG/README.md) · [实现](./Computer_Vision/HOG/hog.py) · [演示](./Computer_Vision/HOG/demo.py) |

<a name="quick-start"></a>

## <img src="./assets/icons/terminal.svg" width="22" height="22" alt=""> Quick Start | 快速开始

### 1. 获取资料与安装依赖

使用 Python 3，按当前代码导入安装所需依赖：

```shell
git clone https://github.com/CCU-Robotics-Association/CRA-Algorithms.git
cd CRA-Algorithms/CRA_Algorithms
python -m pip install numpy matplotlib scipy
```

| 依赖 | 用途 |
| :--- | :--- |
| **NumPy** | 数组、矩阵与数值计算 |
| **Matplotlib** | 演示脚本绘图与可视化 |
| **SciPy** | LQR 中的连续时间代数 Riccati 方程求解 |

### 2. 从 PID 示例开始

在 `CRA_Algorithms` 目录执行：

```shell
python Control/PID/demo.py
```

示例展示一阶系统在 PID 控制下的输出曲线与目标值对比，可结合 `pid.py` 调整控制参数、积分限幅与输出限幅

### 3. 选择其他模块

从算法索引打开对应说明，先查看模型、输入输出与参数，再阅读实现和演示脚本

动力学演示采用包路径导入，在 `CRA_Algorithms` 目录使用模块方式启动，例如：

```shell
python -m Dynamics.RNEA.demo
```

## <img src="./assets/icons/compass.svg" width="22" height="22" alt=""> Study | 阅读建议

- 入门控制可先看 PID，再结合状态空间模型阅读 LQR 与 SMO
- 机械臂部分按正运动学、解析逆解、数值逆解的顺序学习，再阅读动力学
- 腿式机器人部分结合 LIPM、ZMP 与落脚点控制，对照各模块的模型假设
- 碰撞检测与计算机视觉可按索引独立阅读，对比参数变化与演示结果

## <img src="./assets/icons/wrench.svg" width="22" height="22" alt=""> Maintenance | 资料维护

<table>
<tr>
<td width="50%" valign="top">

<img src="./assets/icons/file-text.svg" width="28" height="28" alt="">

### Structure | 模块结构

**算法说明 · Python 实现 · 演示脚本**

沿用 `分类/算法名称/` 结构，说明文件使用 `README.md`，演示脚本使用 `demo.py`

</td>
<td width="50%" valign="top">

<img src="./assets/icons/circle-check.svg" width="28" height="28" alt="">

### Check | 内容检查

**模型假设 · 输入输出 · 参数 · 依赖与导入**

新增或修改模块后核对说明与代码，检查示例入口，并同步更新算法索引

</td>
</tr>
</table>

---

<div align="center">

### CCU · ROBOTICS · ASSOCIATION

<sub>机器人算法资料 | CRA Algorithms</sub>

[**官网(Website)**](https://ccu-robotics-association.github.io/) · [**GitHub 主页**](https://github.com/CCU-Robotics-Association) · [**算法索引(Index)**](#algorithms)

<sub>CCU Robotics Association</sub>

</div>
