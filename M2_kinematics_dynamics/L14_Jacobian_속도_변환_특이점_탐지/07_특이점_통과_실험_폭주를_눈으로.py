# [CH2 Physical AI] 14강. [실습] Jacobian 속도 변환·특이점 탐지
# 절: 특이점 통과 실험 — 폭주를 눈으로
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

m = singularity_metrics(J)
lam = 0.0 if m["sigma_min"] > 0.05 else 0.1 * (1 - m["sigma_min"] / 0.05)
