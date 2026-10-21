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


def jacobian_numeric(fk, thetas, eps=1e-6):
    th = np.asarray(thetas, float)
    x0 = np.asarray(fk(th))
    J = np.zeros((x0.size, th.size))
    for j in range(th.size):
        d = np.zeros_like(th); d[j] = eps
        J[:, j] = (np.asarray(fk(th + d)) - np.asarray(fk(th - d))) / (2 * eps)
    return J


def singularity_metrics(J):
    U, s, Vt = np.linalg.svd(J)
    w = np.sqrt(max(np.linalg.det(J @ J.T), 0.0))   # 조작성
    return {"manipulability": w,
            "sigma_min": s[-1],
            "condition": s[0] / s[-1] if s[-1] > 0 else np.inf}


def dls(J, xdot, lam=0.05):
    """damped least squares (14강 특이점 통과 실험 (나))"""
    JT = J.T
    return JT @ np.linalg.solve(J @ JT + lam**2 * np.eye(J.shape[0]), xdot)


def adaptive_lambda(J):
    """14강: sigma_min 이 작아질 때만 감쇠를 켜는 가변 lambda."""
    m = singularity_metrics(J)
    return 0.0 if m["sigma_min"] > 0.05 else 0.1 * (1 - m["sigma_min"] / 0.05)
