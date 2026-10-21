# [CH2 Physical AI] 14강. [실습] Jacobian 속도 변환·특이점 탐지
# 절: 2. 속도 변환 — 정방향과 역방향
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# 정방향: 관절 속도 -> 손끝 속도
J = jacobian_planar(arm.L, th)
xdot = J @ thdot

# 역방향(속도 IK): 손끝 속도 -> 관절 속도
thdot = np.linalg.pinv(J) @ xdot_desired
