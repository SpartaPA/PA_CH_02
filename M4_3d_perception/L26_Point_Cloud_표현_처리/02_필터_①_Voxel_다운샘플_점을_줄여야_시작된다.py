# [CH2 Physical AI] 26강. Point Cloud 표현·처리 (PCL/Open3D·필터·세그멘테이션)
# 절: 2. 필터 ① Voxel 다운샘플 — 점을 줄여야 시작된다
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

down = pcd.voxel_down_sample(voxel_size=0.01)     # 1cm 격자
