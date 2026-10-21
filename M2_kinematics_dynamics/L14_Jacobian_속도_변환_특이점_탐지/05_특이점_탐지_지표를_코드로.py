# [CH2 Physical AI] 14강. [실습] Jacobian 속도 변환·특이점 탐지
# 절: 3. 특이점 탐지 — 지표를 코드로
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

def singularity_metrics(J):
    U, s, Vt = np.linalg.svd(J)
    w = np.sqrt(max(np.linalg.det(J @ J.T), 0.0))   # 조작성
    return {"manipulability": w,
            "sigma_min": s[-1],
            "condition": s[0] / s[-1] if s[-1] > 0 else np.inf}
