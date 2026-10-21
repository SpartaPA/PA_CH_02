# [CH2 Physical AI] 30강. [실습] Point Cloud 필터링(Voxel/SOR) + RANSAC 평면·클러스터링
# 절: 4. 실데이터 적용과 시각화
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

o3d.visualization.draw_geometries([table.paint_uniform_color([.7,.7,.7])] +
    [colorize(c, k) for k, c in enumerate(clusters)] +
    [aabb_lineset(c) for c in clusters])
