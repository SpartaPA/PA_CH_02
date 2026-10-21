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


# 13강 4-3: z축 오프셋이 있는 3DOF (베이스 회전 + 평면 2링크): D-H로는 alpha=90° 한 행 추가
class Arm3D(PlanarArm):
    def fk_all(self, thetas):
        T = dh_transform(thetas[0], 0.15, 0.0, np.pi/2)   # 허리 회전
        Ts = [T]
        for L, th in zip(self.L, thetas[1:]):
            T = T @ dh_transform(th, 0.0, L, 0.0)
            Ts.append(T)
        return Ts

    def fk(self, thetas):
        """엔드이펙터의 (x, y, z) 위치."""
        return self.fk_all(thetas)[-1][:3, 3]
