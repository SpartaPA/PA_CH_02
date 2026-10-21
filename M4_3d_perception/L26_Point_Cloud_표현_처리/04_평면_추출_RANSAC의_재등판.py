# [CH2 Physical AI] 26강. Point Cloud 표현·처리 (PCL/Open3D·필터·세그멘테이션)
# 절: 4. 평면 추출 — RANSAC의 재등판
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

plane, inliers = clean.segment_plane(distance_threshold=0.01,
                                     ransac_n=3, num_iterations=1000)
table = clean.select_by_index(inliers)            # 평면 (테이블)
objects = clean.select_by_index(inliers, invert=True)   # 나머지 (물체들!)
