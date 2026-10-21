# [CH2 Physical AI] 30강. [실습] Point Cloud 필터링(Voxel/SOR) + RANSAC 평면·클러스터링
# 절: 1. 합성 장면 발생기 — 정답 있는 실험대
# 원본 경로: src/synth_scene.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/synth_scene.py
def make_table_scene(n_noise=300, seed=0):
    """테이블 평면 + 물체 3개(상자2·원기등1) + 허공 노이즈. 정답 dict 반환."""
    rng = np.random.default_rng(seed)
    pts = [sample_plane(2.0, 1.2, n=20000, z=0.0)]           # 테이블
    truth = []
    for center, size in [((0.3, 0.2), (0.10, 0.08, 0.12)),   # 상자1
                         ((-0.2, 0.1), (0.06, 0.06, 0.20)),  # 상자2(길죽)
                         ((0.0, -0.3), (0.08, 0.08, 0.10))]: # 원기등
        pts.append(sample_box(center, size, n=4000))
        truth.append({"center": center, "size": size})
    pts.append(rng.uniform([-1, -0.6, 0], [1, 0.6, 0.5], (n_noise, 3)))  # 허공 점
    return np.vstack(pts), truth
