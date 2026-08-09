---
layout: post
title: UMAT-HILL48-CHABOCHE模型
subtitle: 记录下相关理论
date: 2026-08-09T21:29:00+08:00
author: GuoZiqiang198
header-img: /img/lluvia-rain-header.png
header-mask: 0.35
catalog: true
mathjax: true
tags:
  - UMAT
---

## 二、本构模型（论文正文可直接改写）

### 2.1 屈服函数与流动法则（中文版）

采用 Hill48 二次屈服准则，屈服函数表示为

$$f=\sqrt{\boldsymbol{s}^{\mathrm{T}}\boldsymbol{P}\boldsymbol{s}}-\sigma_y(p)=0,\qquad \boldsymbol{s}=\boldsymbol{\sigma}-\boldsymbol{\alpha}$$

其中 $\boldsymbol{\sigma}$ 为 Cauchy 应力，$\boldsymbol{\alpha}=\sum_{i}\boldsymbol{\alpha}_i$ 为背应力张量（$i=1,2,3$），$\boldsymbol{s}$ 为相对应力，$p$ 为累积等效塑性应变。Hill48 矩阵 $\boldsymbol{P}$ 在工程剪切 Voigt 记法下为

$$\boldsymbol{P}=\begin{bmatrix}
G+H & -H & -G & 0 & 0 & 0\
 & F+H & -F & 0 & 0 & 0\
 & & F+G & 0 & 0 & 0\
 & \mathrm{sym} & & 2N & 0 & 0\
 & & & & 2M & 0\
 & & & & & 2L
\end{bmatrix}$$

根据关联流动法则，塑性应变速率为

$$\dot{\boldsymbol{\varepsilon}}^p=\dot\lambda,\frac{\partial f}{\partial\boldsymbol{s}},\qquad f=\bar\sigma-Y$$

对 $\bar\sigma=\sqrt{\boldsymbol{s}^{\mathrm{T}}\boldsymbol{P}\boldsymbol{s}}$ 求导（$\partial(\boldsymbol{s}^{\mathrm{T}}\boldsymbol{P}\boldsymbol{s})/\partial\boldsymbol{s}=2\boldsymbol{P}\boldsymbol{s}$，$\boldsymbol{P}$ 对称）：

$$\frac{\partial f}{\partial\boldsymbol{s}}=\frac{\partial\bar\sigma}{\partial\boldsymbol{s}}=\frac{\boldsymbol{P}\boldsymbol{s}}{\bar\sigma}$$

代入得

$$\dot{\boldsymbol{\varepsilon}}^p=\dot\lambda,\frac{\boldsymbol{P}\boldsymbol{s}}{\bar\sigma}$$

$\bar\sigma(\boldsymbol{s})$ 是 $\boldsymbol{s}$ 的一次齐次函数，由欧拉齐次定理

$$\boldsymbol{s}:\frac{\partial\bar\sigma}{\partial\boldsymbol{s}}=\bar\sigma$$

结合关联流动法则 $\dot{\boldsymbol{\varepsilon}}^p=\dot\lambda,\partial\bar\sigma/\partial\boldsymbol{s}$ 及功共轭定义 $\dot p=\boldsymbol{s}:\dot{\boldsymbol{\varepsilon}}^p/\bar\sigma$，得 $\dot\lambda=\dot p$。于是塑性应变速率为

$$\dot{\boldsymbol{\varepsilon}}^p=\dot p,\frac{\boldsymbol{P}\boldsymbol{s}}{\bar\sigma}$$

采用向后欧拉积分，塑性应变增量写为

$$\Delta\boldsymbol{\varepsilon}^p=\Delta p,\frac{\boldsymbol{P}\boldsymbol{s}}{\bar\sigma}$$

### 2.2 硬化演化

各向同性硬化采用 Voce 形式（$Q_\infty<0$ 时描述循环软化）：

$$\sigma_y(p)=\sigma_0+Q_\infty\left(1-e^{-bp}\right)$$

非线性随动硬化采用三个 Armstrong–Frederick 背应力叠加：

$$\dot{\boldsymbol{\alpha}}_i=\frac{2}{3}C_i\dot{\boldsymbol{\varepsilon}}^p-\gamma_i\boldsymbol{\alpha}_i\dot p,\qquad i=1,2,3$$

在增量内对上述方程做向后欧拉积分（令增量内 $d\boldsymbol{\varepsilon}^p=\Delta\lambda,\hat{\boldsymbol{n}}$、$dp=\Delta\lambda$，恢复项中的 $\boldsymbol{\alpha}_k$ 取增量终点值，隐式、无条件稳定），背应力的隐式更新为

$$\boldsymbol{\alpha}{k,new}_=\frac{\boldsymbol{\alpha}_{k,old}+\frac{2}{3}C_k,\Delta\lambda,\hat{\boldsymbol{n}}}{1+\gamma_k,\Delta\lambda}$$

推导如下：由演化方程

$$\boldsymbol{\alpha}_k^{new}-\boldsymbol{\alpha}_{k,old}=\frac{2}{3}C_k,\Delta\lambda,\hat{\boldsymbol{n}}-\gamma_k,\boldsymbol{\alpha}_k^{new},\Delta\lambda$$

移项后即得上式。该格式对该线性常微分方程为精确积分；当 $\Delta\lambda\to\infty$ 时 $\boldsymbol{\alpha}_k$ 趋于饱和值 $(2/3)(C_k/\gamma_k),\hat{\boldsymbol{n}}$。

弹性模量退化（Yoshida–Uemori 形式）：

$$E(p)=E_A+(E_0-E_A)e^{-\xi p}$$

### 2.3 断裂准则

断裂准则采用 Bai–Wierzbicki (2008) 应力状态相关断裂应变：

$$\bar\varepsilon_f=\left[\frac{F_1+F_5}{2}-F_3\right]\bar\theta^2+\frac{F_1-F_5}{2}\bar\theta+F_3$$

其中 $F_1=D_1e^{-D_2\eta}$、$F_3=D_3e^{-D_4\eta}$、$F_5=D_5e^{-D_6\eta}$，$\eta$ 为应力三轴度，$\bar\theta$ 为归一化 Lode 角参数；损伤按 $D=\sum\Delta\lambda/\bar\varepsilon_f$ 累积，$D\geq1$ 判为断裂。

### 2.4 数值积分算法（完全隐式最近点投影、CPPM）

在每个增量步内，给定增量应变 $\Delta\boldsymbol{\varepsilon}$ 与上一收敛状态
${\boldsymbol{\varepsilon}^p_{old},,\boldsymbol{\alpha}_{i,old},,p_{old}}$，未知量为 **7 个**：

$$\boldsymbol{X}=\left[s_1,\ s_2,\ s_3,\ s_4,\ s_5,\ s_6,\ \Delta\lambda\right]^{\mathrm{T}}$$

即相对应力 6 个分量与塑性乘子增量 $\Delta\lambda$。其满足的 7 个非线性残差方程 $\boldsymbol{R}(\boldsymbol{X})=\boldsymbol{0}$ 为：

**(1) 应力更新方程（6 个）**——"弹性试算 + 返回映射"：

**弹性试算（elastic predictor）**：增量内先假定完全弹性——塑性应变保持上一增量末值
$\boldsymbol{\varepsilon}^p_{old}$，弹性应变试算值为增量末总应变减去塑性应变：

$$\boldsymbol{\varepsilon}^{e,tr}=\boldsymbol{\varepsilon}_{old}+\Delta\boldsymbol{\varepsilon}-\boldsymbol{\varepsilon}^p_{old}$$

试算应力由该弹性应变与当前弹性刚度给出：

$$\boldsymbol{\sigma}^{tr}=\boldsymbol{C}!\left(E!\left(p_{old}+\Delta\lambda\right)\right)\cdot\boldsymbol{\varepsilon}^{e,tr}$$

其中 $\boldsymbol{C}$ 为各向同性弹性刚度，弹性模量 $E$ 取当前硬化状态 $p_{old}+\Delta\lambda$（试算应力随 $\Delta\lambda$ 的迭代而更新，$E(p)$ 隐式依赖 $\Delta\lambda$）。若 $\bar\sigma(\boldsymbol{\sigma}^{tr}-\sum\boldsymbol{\alpha}_{old})\leq\sigma_y(p_{old})$，则为弹性步，直接取 $\boldsymbol{\sigma}=\boldsymbol{\sigma}^{tr}$；否则进入塑性返回。

**塑性返回（return mapping）**：塑性流动使应力返回屈服面，返回后的应力满足

$$\boldsymbol{\sigma}=\boldsymbol{\sigma}^{tr}-\Delta\lambda,\boldsymbol{C}\boldsymbol{n}=\boldsymbol{s}+\sum_{k}\boldsymbol{\alpha}_k^{new}$$

故相对应力 $\boldsymbol{s}$ 的求解方程（6 个残差分量）为：

$$R_i=s_i-\sigma^{\mathrm{tr}}_i+\Delta\lambda,C_{ij}n_j+\sum_{k=1}^{3}\alpha_{i,k}^{new}=0,\qquad i=1,\dots,6$$

其中背应力 $\boldsymbol{\alpha}_k^{new}$ 按 §2.2 给出的隐式更新式计算（向后欧拉）。

流动方向 $\boldsymbol{n}=\boldsymbol{P}\boldsymbol{s}/\bar\sigma$；$\hat{\boldsymbol{n}}$ 用于背应力张量演化。$\boldsymbol{n}$ 即屈服面外法线（关联流动），其推导如下：由 $\bar\sigma^2=\boldsymbol{s}^{\mathrm{T}}\boldsymbol{P}\boldsymbol{s}$ 对 $\boldsymbol{s}$ 求导（$\boldsymbol{P}$ 对称），得 $2\bar\sigma,\partial\bar\sigma/\partial\boldsymbol{s}=2\boldsymbol{P}\boldsymbol{s}$，即

$$\boldsymbol{n}=\frac{\partial\bar\sigma}{\partial\boldsymbol{\sigma}}=\frac{\boldsymbol{P}\boldsymbol{s}}{\bar\sigma}$$

**(2) 屈服一致性条件（1 个）**：

$$R_7=\bar\sigma(\boldsymbol{s})-\sigma_y!\left(p_{old}+\Delta\lambda\right)=0$$

**(3) Newton–Raphson 迭代**：每次迭代组装 7×7 Jacobian 矩阵 $\boldsymbol{J}=\partial\boldsymbol{R}/\partial\boldsymbol{X}$：

$$\frac{\partial R_i}{\partial s_j}=\delta_{ij}+\Delta\lambda,C_{ik}\frac{\partial n_k}{\partial s_j}
+\sum_{k=1}^{3}\frac{\frac{2}{3}C_k,\Delta\lambda}{1+\gamma_k\Delta\lambda},\frac{\partial\hat{n}_i}{\partial s_j}$$

其中流动方向的导数由

$$\frac{\partial n}{\partial\boldsymbol{s}}=\frac{\boldsymbol{P}-\boldsymbol{n}\otimes\boldsymbol{n}}{\bar\sigma}$$

给出。

$$\frac{\partial R_i}{\partial\Delta\lambda}=\left(\boldsymbol{C}\boldsymbol{n}\right)_i-\frac{E'}{E}\sigma_i
+\sum_{k=1}^{3}\frac{\frac{2}{3}C_k,\hat{n}_i-\gamma_k,\alpha_{k,old,i}}{\left(1+\gamma_k,\Delta\lambda\right)^2}$$

$$\frac{\partial R_7}{\partial\boldsymbol{s}}=\boldsymbol{n}^{\mathrm{T}}$$

$$\frac{\partial R_7}{\partial\Delta\lambda}=-H!\left(p_{old}+\Delta\lambda\right)$$

求解线性方程组 $\boldsymbol{J}\cdot\Delta\boldsymbol{X}=-\boldsymbol{R}$，更新 $\boldsymbol{X}\leftarrow\boldsymbol{X}+\Delta\boldsymbol{X}$。

**(4) 线搜索（软化段收敛的关键）**：若试探步不使残差范数下降，即
$|\boldsymbol{R}(\boldsymbol{X}+\Delta\boldsymbol{X})|\geq|\boldsymbol{R}(\boldsymbol{X})|$，则步长折半（$\Delta\boldsymbol{X}\leftarrow\Delta\boldsymbol{X}/2$）后重试，保证残差范数单调下降。
该策略对 $Q_\infty<0$（循环软化，局部刚度非正定）工况的收敛至关重要。

**(5) 收敛判据**：$\max_i|R_i|/\sigma_0<10^{-9}$（残差按初始屈服应力归一化）。

收敛后更新：$\boldsymbol{\sigma}=\boldsymbol{s}+\sum_k\boldsymbol{\alpha}_k^{new}$（等价于 $\boldsymbol{\sigma}=\boldsymbol{\sigma}^{tr}-\Delta\lambda,\boldsymbol{C}\boldsymbol{n}$）、$\boldsymbol{\varepsilon}^p\leftarrow\boldsymbol{\varepsilon}^p+\Delta\lambda,\boldsymbol{n}$、$p\leftarrow p+\Delta\lambda$；算法切向刚度 DDSDDE 由局部方程组对 $\boldsymbol{\varepsilon}$ 的全微分（Schur 补）导出，本实现采用"冻结 $E$"变体（省略 $\partial E/\partial p$ 项以保证与隐式积分严格一致时仍接近二次收敛），在 Abaqus 中以 UNSYMM 求解器调用。有限变形采用 Jaumann 率协转框架处理。

> 引用建议：若为英文论文，可将 2.1–2.2 的公式直接翻译为英文（方程不变），并在正文注明 "implemented in a user material subroutine (UMAT) for Abaqus/Standard"。
