# [CH2 Physical AI] 13강. [실습] 2~3DOF FK 동차변환 체인
# 절: 1. 기본 변환 블록 만들기
# 원본 경로: src/transforms.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/transforms.py  (Lv.1 모듈의 재사용 + 보강)
import numpy as np

def rot_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0],
                     [0, 0, 1, 0], [0, 0, 0, 1.0]])

def rot_x(alpha):
    c, s = np.cos(alpha), np.sin(alpha)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0],
                     [0, s, c, 0], [0, 0, 0, 1.0]])

def trans(x=0.0, y=0.0, z=0.0):
    T = np.eye(4); T[:3, 3] = [x, y, z]
    return T
