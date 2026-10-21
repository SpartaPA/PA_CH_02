# [CH2 Physical AI] 30강. [실습] Point Cloud 필터링(Voxel/SOR) + RANSAC 평면·클러스터링
# 절: 2. 파이프라인 조립 — 단계마다 계량
# 원본 경로: src/segment.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/segment.py
def segment_objects(pcd, voxel=0.01, sor_k=20, sor_std=2.0,
                    plane_dist=0.01, eps=0.03, min_pts=30):
    log = {}
    t0 = time.perf_counter()
    down = pcd.voxel_down_sample(voxel);            log["voxel"] = stat(down, t0)
    clean, _ = down.remove_statistical_outlier(sor_k, sor_std)
    log["sor"] = stat(clean, t0)
    plane, inl = clean.segment_plane(plane_dist, 3, 1000)
    objects = clean.select_by_index(inl, invert=True)
    log["plane"] = stat(objects, t0)
    labels = np.array(objects.cluster_dbscan(eps, min_pts))
    log["cluster"] = stat(objects, t0)
    out = []
    for k in range(labels.max() + 1):
        c = objects.select_by_index(np.where(labels == k)[0])
        aabb = c.get_axis_aligned_bounding_box()
        out.append({"center": aabb.get_center(), "size": aabb.get_extent(),
                    "n_pts": len(c.points)})
    return out, log
