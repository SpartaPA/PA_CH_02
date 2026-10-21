# [CH2 Physical AI] 26강. Point Cloud 표현·처리 (PCL/Open3D·필터·세그멘테이션)
# 절: 1. 표현 — 순서 없는 점들의 집합
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

import open3d as o3d
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)     # (N, 3) ndarray
o3d.visualization.draw_geometries([pcd])
