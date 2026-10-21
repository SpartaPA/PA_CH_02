# 13강 4절: 자세 그리기 + 작업 공간(몬테카를로) + 3D 확장  →  demos/out/fk_workspace.png
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.fk_chain import PlanarArm, Arm3D


def draw_arm(ax, arm, thetas, **kw):
    pts = np.array([[0, 0]] + [T[:2, 3] for T in arm.fk_all(thetas)])
    ax.plot(pts[:, 0], pts[:, 1], "-o", lw=3, ms=8, **kw)


arm = PlanarArm([0.3, 0.2])
print("fk([0,0])    =", arm.fk([0, 0]))            # [0.5 0. ]
print("fk([pi/2,0]) =", arm.fk([np.pi / 2, 0]))    # [0.  0.5]
print("Arm3D fk     =", Arm3D([0.3, 0.2]).fk([np.pi / 4, 0.3, -0.6]))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 5))
for th in [(0, 0), (np.pi / 4, np.pi / 4), (np.pi / 2, -np.pi / 2)]:
    draw_arm(a1, arm, th, label=f"theta={np.round(th, 2)}")
a1.set_aspect("equal"); a1.legend(); a1.set_title("Poses (FK)")

rng = np.random.default_rng(0)
ths = rng.uniform(-np.pi, np.pi, size=(20000, 2))
pts = np.array([arm.fk(t) for t in ths])
a2.scatter(pts[:, 0], pts[:, 1], s=1, alpha=0.2)
a2.set_aspect("equal"); a2.set_title("Workspace (Monte Carlo)")

os.makedirs(os.path.join(os.path.dirname(__file__), "out"), exist_ok=True)
fig.savefig(os.path.join(os.path.dirname(__file__), "out", "fk_workspace.png"), dpi=120)
r = np.linalg.norm(pts, axis=1)
print(f"reach: min={r.min():.3f}  max={r.max():.3f}  (이론: 0.1 ~ 0.5)")
