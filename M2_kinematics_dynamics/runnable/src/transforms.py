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


def dh_transform(theta, d, a, alpha):
    """standard D-H 한 행의 T_{i-1 -> i}"""
    return rot_z(theta) @ trans(z=d) @ trans(x=a) @ rot_x(alpha)
