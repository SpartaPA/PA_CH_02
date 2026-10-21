# [CH2 Physical AI] 16강. OpenCV 기초 (입출력·HSV·필터링·모폴로지)
# 절: 2. 색공간 — 왜 HSV인가
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255))   # 빨강 범위 → 이진 마스크
