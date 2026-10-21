# [CH2 Physical AI] 26강. Point Cloud 표현·처리 (PCL/Open3D·필터·세그멘테이션)
# 절: 3. 필터 ② SOR — 통계로 이상치 걷어내기
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

clean, idx = down.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
