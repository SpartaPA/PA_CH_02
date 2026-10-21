# [CH2 Physical AI] 17강. 핀홀 카메라 모델과 렌즈 왜곡 (내부파라미터 K·방사/접선)
# 절: 언제 반드시 보정해야 하나
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

undistorted = cv2.undistort(img, K, dist_coeffs)          # 이미지 전체 보정
pts_norm = cv2.undistortPoints(pts, K, dist_coeffs)       # 점만 보정 (빠름, PnP 전처리)
