# [CH2 Physical AI] 14강. [실습] Jacobian 속도 변환·특이점 탐지
# 절: 1-2. 수치 미분 Jacobian — 검증자
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

def jacobian_numeric(fk, thetas, eps=1e-6):
    th = np.asarray(thetas, float)
    x0 = np.asarray(fk(th))
    J = np.zeros((x0.size, th.size))
    for j in range(th.size):
        d = np.zeros_like(th); d[j] = eps
        J[:, j] = (np.asarray(fk(th + d)) - np.asarray(fk(th - d))) / (2 * eps)
    return J
