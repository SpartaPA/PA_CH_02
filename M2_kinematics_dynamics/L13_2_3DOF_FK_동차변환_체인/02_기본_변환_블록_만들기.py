# [CH2 Physical AI] 13강. [실습] 2~3DOF FK 동차변환 체인
# 절: 1. 기본 변환 블록 만들기
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

def dh_transform(theta, d, a, alpha):
    """standard D-H 한 행의 T_{i-1 -> i}"""
    return rot_z(theta) @ trans(z=d) @ trans(x=a) @ rot_x(alpha)
