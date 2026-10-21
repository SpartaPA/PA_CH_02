# [CH2 Physical AI] 14강. [실습] Jacobian 속도 변환·특이점 탐지
# 절: 1-1. 해석적 Jacobian
# 원본 경로: src/jacobian.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/jacobian.py
import numpy as np

def jacobian_planar(L, thetas):
    """평면 회전 팔의 2xN Jacobian. L: 링크 길이 목록."""
    L = np.asarray(L, float); th = np.asarray(thetas, float)
    cum = np.cumsum(th)                       # theta1, theta1+theta2, ...
    J = np.zeros((2, len(L)))
    for j in range(len(L)):
        # j열 = j번째 이후 링크들이 만드는 회전 반경의 90° 회전
        J[0, j] = -(L[j:] * np.sin(cum[j:])).sum()
        J[1, j] =  (L[j:] * np.cos(cum[j:])).sum()
    return J
