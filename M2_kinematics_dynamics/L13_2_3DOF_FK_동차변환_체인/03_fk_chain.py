# [CH2 Physical AI] 13강. [실습] 2~3DOF FK 동차변환 체인
# 절: 2. FK 체인 — 로봇을 데이터로 표현하기
# 원본 경로: src/fk_chain.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/fk_chain.py
import numpy as np
from .transforms import dh_transform

class PlanarArm:
    """회전 조인트 평면 팔. dh_rows: (d, a, alpha) 상수부 목록."""
    def __init__(self, link_lengths):
        self.L = list(link_lengths)              # [L1, L2, (L3)]

    def fk_all(self, thetas):
        """각 링크 좌표계의 T^0_i 목록을 반환 (시각화용)."""
        Ts, T = [], np.eye(4)
        for L, th in zip(self.L, thetas):
            T = T @ dh_transform(th, 0.0, L, 0.0)
            Ts.append(T)
        return Ts

    def fk(self, thetas):
        """엔드이펙터의 (x, y) 위치."""
        return self.fk_all(thetas)[-1][:2, 3]
