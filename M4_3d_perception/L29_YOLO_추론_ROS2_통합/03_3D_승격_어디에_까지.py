# [CH2 Physical AI] 29강. [실습] YOLO 추론 ROS2 통합
# 절: 4. 3D 승격 — "어디에"까지
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# 박스 밑변 중심 → 바닥 평면 교점 (23강 geometry.py 재사용)
u, v = det.bbox.center.position.x, det.bbox.center.position.y + det.bbox.size_y / 2
P_world = ray_plane_intersect(u, v, K, T_world_cam, plane_z=0.0)
