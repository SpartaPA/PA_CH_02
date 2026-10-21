# [CH2 Physical AI] 14강. [실습] Jacobian 속도 변환·특이점 탐지
# 절: 특이점 통과 실험 — 폭주를 눈으로
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

thdot = np.linalg.pinv(J) @ xdot          # (가) 순정 pinv
# vs
def dls(J, xdot, lam=0.05):
    JT = J.T                               # (나) damped least squares
    return JT @ np.linalg.solve(J @ JT + lam**2 * np.eye(J.shape[0]), xdot)
