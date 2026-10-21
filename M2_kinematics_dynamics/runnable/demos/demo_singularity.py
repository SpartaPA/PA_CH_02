# 14강: 특이점 통과 실험 — 순정 pinv vs DLS  →  demos/out/singularity.png
# 손끝을 반경 방향 바깥으로 밀어 팔이 쭉 펴지는(θ2→0) 경계 특이점으로 몰아간다.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.fk_chain import PlanarArm
from src.jacobian import jacobian_planar, singularity_metrics, dls, adaptive_lambda

arm = PlanarArm([0.3, 0.2])
dt, steps = 0.01, 400
TH0 = np.array([0.3, -0.8])                      # 손끝 반경 ≈ 0.46 m (최대 도달 0.5 m)
p0 = arm.fk(TH0)
xdot = 0.02 * p0 / np.linalg.norm(p0)            # 반경 방향 바깥으로 2 cm/s → 약 2 s 뒤 경계 도달

def run(solver):
    th = TH0.copy(); log = []
    for _ in range(steps):
        J = jacobian_planar(arm.L, th)
        thdot = solver(J)
        th = th + thdot * dt
        log.append((np.abs(thdot).max(), singularity_metrics(J)["manipulability"]))
    return np.array(log)

pinv = run(lambda J: np.linalg.pinv(J) @ xdot)
damp = run(lambda J: dls(J, xdot, lam=adaptive_lambda(J)))

t = np.arange(steps) * dt
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
a1.semilogy(t, pinv[:, 0], label="pinv"); a1.semilogy(t, damp[:, 0], label="DLS (adaptive lambda)")
a1.set_ylabel("max |dtheta/dt| [rad/s]"); a1.legend()
a2.plot(t, pinv[:, 1], label="pinv"); a2.plot(t, damp[:, 1], label="DLS")
a2.set_ylabel("manipulability w"); a2.set_xlabel("t [s]")
os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
fig.savefig(os.path.join(os.path.dirname(__file__), "out", "singularity.png"), dpi=120)
print(f"peak |θ̇|  pinv={pinv[:,0].max():.2f}  DLS={damp[:,0].max():.2f} rad/s")
