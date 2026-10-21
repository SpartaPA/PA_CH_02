# [CH2 Physical AI] 31강. [실습] RGBD 깊이 취득·포인트클라우드 변환
# 절: 4. 합류 — 검출×깊이×클라우드
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

color, depth = src.read()
dets = yolo(color)                                   # 29강
for det in dets:
    u0, v0, u1, v1 = box_of(det)
    roi_depth = depth[v0:v1, u0:u1]                  # 박스 안 깊이만
    xyz, rgb = depth_to_cloud(roi_depth, K_shifted(K, u0, v0), color[v0:v1, u0:u1])
    cands, _ = segment_objects(to_o3d(xyz, rgb))     # 30강 (ROI라 평면 단계는 선택)
    # 가장 큰 후보의 중심 = 물체 3D 위치 (정밀!), 크기 = 실측
