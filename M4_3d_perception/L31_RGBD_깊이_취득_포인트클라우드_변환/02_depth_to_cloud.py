# [CH2 Physical AI] 31강. [실습] RGBD 깊이 취득·포인트클라우드 변환
# 절: 2. 역투영 — 30만 픽셀을 한 번에
# 원본 경로: src/depth_to_cloud.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/depth_to_cloud.py
def depth_to_cloud(depth, K, color=None, z_min=0.15, z_max=3.0):
    H, W = depth.shape
    u, v = np.meshgrid(np.arange(W), np.arange(H))          # 픽셀 격자
    valid = (depth > z_min) & (depth < z_max)               # 0(무효)·범위 밖 제거
    z = depth[valid]
    x = (u[valid] - K[0, 2]) * z / K[0, 0]                  # 전 픽셀 동시 역투영
    y = (v[valid] - K[1, 2]) * z / K[1, 1]
    xyz = np.stack([x, y, z], axis=1)                        # (N, 3)
    rgb = color[valid][:, ::-1] / 255.0 if color is not None else None
    return xyz, rgb
