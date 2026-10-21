# src/arm_dynamics.py
# 15강 시뮬레이터: 12강 동역학 표준형  M(θ)θ̈ + C(θ,θ̇)θ̇ + g(θ) = τ  를 한 스텝씩 적분.
# 교안은 step()만 보여 주고 M/C/gvec는 생략(...)했으므로, 여기서는
# "링크 끝에 질량이 몰린 수직 평면 2링크 팔"(θ는 수평 기준) 모델로 채웠다.
import numpy as np


class TwoLinkDynamics:
    def __init__(self, m=(1.0, 0.8), L=(0.3, 0.2), g=9.81):
        self.m1, self.m2 = m
        self.L1, self.L2 = L
        self.g = g
        self.th = np.zeros(2)
        self.thd = np.zeros(2)

    def M(self, th):
        """2x2 관성 행렬 (자세 의존) — cos θ2 항: 팔꿈치를 펴면 최대."""
        m1, m2, L1, L2 = self.m1, self.m2, self.L1, self.L2
        c2 = np.cos(th[1])
        m11 = m1 * L1**2 + m2 * (L1**2 + L2**2 + 2 * L1 * L2 * c2)
        m12 = m2 * (L2**2 + L1 * L2 * c2)
        m22 = m2 * L2**2
        return np.array([[m11, m12], [m12, m22]])

    def C(self, th, thd):
        """코리올리·원심 행렬 (C θ̇ 형태로 사용)."""
        h = self.m2 * self.L1 * self.L2 * np.sin(th[1])
        return np.array([[-h * thd[1], -h * (thd[0] + thd[1])],
                         [h * thd[0], 0.0]])

    def gvec(self, th):
        """중력 토크 — 수평일 때 최대, 수직일 때 0."""
        c1, c12 = np.cos(th[0]), np.cos(th[0] + th[1])
        g2 = self.m2 * self.g * self.L2 * c12
        g1 = (self.m1 + self.m2) * self.g * self.L1 * c1 + g2
        return np.array([g1, g2])

    def energy(self):
        """운동에너지 + 위치에너지 (감쇠 없을 때 보존되어야 함)."""
        th, thd = self.th, self.thd
        ke = 0.5 * thd @ self.M(th) @ thd
        y1 = self.L1 * np.sin(th[0])
        y2 = y1 + self.L2 * np.sin(th[0] + th[1])
        pe = self.g * (self.m1 * y1 + self.m2 * y2)
        return ke + pe

    # ---- 아래 step()은 교안 원문 그대로 (semi-implicit Euler) ----
    def step(self, tau, dt=1e-3):
        thdd = np.linalg.solve(self.M(self.th),
                               tau - self.C(self.th, self.thd) @ self.thd
                                   - self.gvec(self.th))
        self.thd += thdd * dt
        self.th  += self.thd * dt

    # ---- 보강: RK4 적분 (교안의 오일러는 큰 진폭 자유 진동에서 에너지가 수십 % 새어 나감) ----
    def _f(self, th, thd, tau):
        return np.linalg.solve(self.M(th), tau - self.C(th, thd) @ thd - self.gvec(th))

    def step_rk4(self, tau, dt=1e-3):
        th, thd = self.th.copy(), self.thd.copy()
        k1v, k1a = thd, self._f(th, thd, tau)
        k2v, k2a = thd + dt/2*k1a, self._f(th + dt/2*k1v, thd + dt/2*k1a, tau)
        k3v, k3a = thd + dt/2*k2a, self._f(th + dt/2*k2v, thd + dt/2*k2a, tau)
        k4v, k4a = thd + dt*k3a, self._f(th + dt*k3v, thd + dt*k3a, tau)
        self.th = th + dt/6*(k1v + 2*k2v + 2*k3v + k4v)
        self.thd = thd + dt/6*(k1a + 2*k2a + 2*k3a + k4a)
