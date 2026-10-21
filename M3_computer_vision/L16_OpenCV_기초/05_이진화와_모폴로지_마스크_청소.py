# [CH2 Physical AI] 16강. OpenCV 기초 (입출력·HSV·필터링·모폴로지)
# 절: 4. 이진화와 모폴로지 — 마스크 청소
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
clean = cv2.morphologyEx(clean, cv2.MORPH_CLOSE, kernel)
