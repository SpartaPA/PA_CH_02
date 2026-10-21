# [CH2 Physical AI] 15강. [실습] Quintic 궤적 생성 + PID 튜닝
# 절: 2. 시뮬레이터 — 12강 동역학을 코드로
# 원본 경로: src/arm_dynamics.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/arm_dynamics.py (핵심부)
class TwoLinkDynamics:
    def __init__(self, m=(1.0, 0.8), L=(0.3, 0.2), g=9.81): ...
    def M(self, th):  ...      # 2x2 관성 행렬 (자세 의존)
    def C(self, th, thd): ...  # 코리올리
    def gvec(self, th): ...    # 중력 토크
    def step(self, tau, dt=1e-3):
        thdd = np.linalg.solve(self.M(self.th),
                               tau - self.C(self.th, self.thd) @ self.thd
                                   - self.gvec(self.th))
        self.thd += thdd * dt
        self.th  += self.thd * dt
