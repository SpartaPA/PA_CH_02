# [CH2 Physical AI] 16강. OpenCV 기초 (입출력·HSV·필터링·모폴로지)
# 절: 3. 필터링 — 노이즈를 눌러야 마스크가 깨끗하다
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

smooth = cv2.GaussianBlur(img, (5, 5), 0)     # 커널 크기는 홀수
