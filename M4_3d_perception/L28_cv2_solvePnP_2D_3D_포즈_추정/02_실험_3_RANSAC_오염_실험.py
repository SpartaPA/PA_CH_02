# [CH2 Physical AI] 28강. [실습] cv2.solvePnP 2D-3D 포즈 추정
# 절: 4. 실험 3 — RANSAC 오염 실험
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ok, rvec, tvec, inl = cv2.solvePnPRansac(obj, img, K, None,
                                         reprojectionError=3.0,
                                         iterationsCount=200,
                                         flags=cv2.SOLVEPNP_P3P)
gate = ok and inl is not None and len(inl) >= max(6, 0.4 * len(obj))   # 품질 게이트
