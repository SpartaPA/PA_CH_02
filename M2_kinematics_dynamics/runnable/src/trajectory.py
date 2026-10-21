# src/trajectory.py
import numpy as np

def quintic(theta0, thetaf, T):
    """정지->정지 5차 궤적. t 배열을 받아 (pos, vel, acc)를 돌려주는 함수 반환."""
    d = thetaf - theta0
    a3, a4, a5 = 10*d/T**3, -15*d/T**4, 6*d/T**5
    def eval(t):
        t = np.clip(t, 0.0, T)
        pos = theta0 + a3*t**3 + a4*t**4 + a5*t**5
        vel = 3*a3*t**2 + 4*a4*t**3 + 5*a5*t**4
        acc = 6*a3*t + 12*a4*t**2 + 20*a5*t**3
        return pos, vel, acc
    return eval
