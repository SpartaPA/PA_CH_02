# [CH2 Physical AI] 28강. [실습] cv2.solvePnP 2D-3D 포즈 추정
# 절: 1. 합성 벤치마크 러너
# 원본 경로: src/pnp_bench.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/pnp_bench.py
def make_scene(n_pts, R_true, t_true, K, noise_px=0.5, outlier_ratio=0.0):
    obj = rng.uniform(-0.1, 0.1, (n_pts, 3)).astype(np.float32)   # 물체 좌표 점들
    img = project_points(obj, R_true, t_true, K)                   # 23강 project
    img += rng.normal(0, noise_px, img.shape)                      # 관측 노이즈
    n_out = int(n_pts * outlier_ratio)
    idx = rng.choice(n_pts, n_out, replace=False)
    img[idx] = rng.uniform([0, 0], [640, 480], (n_out, 2))         # 이상치 주입
    return obj, img.astype(np.float32)

def pose_error(rvec, tvec, R_true, t_true):
    R_est, _ = cv2.Rodrigues(rvec)
    dR = R_est @ R_true.T
    ang = np.degrees(np.arccos(np.clip((np.trace(dR) - 1) / 2, -1, 1)))
    return ang, np.linalg.norm(tvec.ravel() - t_true)              # [deg], [m]
