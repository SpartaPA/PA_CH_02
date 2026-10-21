# 15강 3절: 추종 실험 — 계단 vs Quintic, PID vs PID+중력 보상  →  demos/out/tracking.png
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.arm_dynamics import TwoLinkDynamics
from src.trajectory import quintic

Kp, Ki, Kd = np.array([40.0, 20.0]), np.array([10.0, 5.0]), np.array([4.0, 1.5])
th0, thf, T, dt, Tsim = np.zeros(2), np.array([np.pi / 3, np.pi / 4]), 1.5, 1e-3, 3.0
traj = [quintic(th0[i], thf[i], T) for i in range(2)]

def run(use_quintic, gravity_comp):
    sim = TwoLinkDynamics(); sim.th = th0.copy()
    integ = np.zeros(2); ts = np.arange(0, Tsim, dt); err = []; hist = []
    for t in ts:
        if use_quintic:
            ref = np.array([[*f(t)][:2] for f in traj])     # (pos, vel)
            th_ref, thd_ref = ref[:, 0], ref[:, 1]
        else:
            th_ref, thd_ref = thf, np.zeros(2)
        th, thd = sim.th, sim.thd
        integ += (th_ref - th) * dt
        tau = Kp*(th_ref - th) + Kd*(thd_ref - thd) + Ki*integ    # 관절별 PID
        if gravity_comp:
            tau += sim.gvec(th)                                    # (나) 중력 보상 켜기
        sim.step(tau, dt)
        err.append(th_ref - sim.th); hist.append(sim.th.copy())
    return ts, np.array(hist), np.sqrt(np.mean(np.square(err)))

fig, ax = plt.subplots(figsize=(8, 4.5))
for q in (False, True):
    for g in (False, True):
        ts, h, rms = run(q, g)
        name = f"{'Quintic' if q else 'Step'} + {'PID+g' if g else 'PID'}"
        ax.plot(ts, h[:, 0], label=f"{name} (RMS {rms:.3f} rad)")
        print(f"{name:22s} RMS tracking error = {rms:.4f} rad")
ax.axhline(thf[0], color="gray", ls="--"); ax.set_xlabel("t [s]"); ax.set_ylabel("theta1 [rad]"); ax.legend()
os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
fig.savefig(os.path.join(os.path.dirname(__file__), "out", "tracking.png"), dpi=120)
