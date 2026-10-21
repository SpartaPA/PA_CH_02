# [CH2 Physical AI] 24강. PnP 심화 (EPnP·P3P)
# 절: 3. 이상치의 세계 — RANSAC
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ok, rvec, tvec, inliers = cv2.solvePnPRansac(
    obj_pts, img_pts, K, dist,
    reprojectionError=3.0, iterationsCount=100, flags=cv2.SOLVEPNP_P3P)
