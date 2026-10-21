# [CH2 Physical AI] 26강. Point Cloud 표현·처리 (PCL/Open3D·필터·세그멘테이션)
# 절: 5. 클러스터링 — 덩어리를 개체로
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

labels = np.array(objects.cluster_dbscan(eps=0.02, min_points=10))
# labels: 점별 클러스터 번호 (-1 = 노이즈) → 클러스터별 중심·바운딩박스 계산
