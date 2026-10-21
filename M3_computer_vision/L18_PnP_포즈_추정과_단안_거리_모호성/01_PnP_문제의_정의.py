# [CH2 Physical AI] 18강. PnP 포즈 추정과 단안 거리 모호성
# 절: 1. PnP 문제의 정의
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ok, rvec, tvec = cv2.solvePnP(obj_pts, img_pts, K, dist)
