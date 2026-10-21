# [CH2 Physical AI] 20강. [실습] 체커보드 카메라 캘리브레이션 (intrinsic/distortion)
# 절: 2. 코너 검출과 캘리브레이션 실행
# 원본 경로: scripts/calibrate.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# scripts/calibrate.py (핵심부)
import cv2, glob
import numpy as np

CB = (9, 6)                                   # 내부 코너 수
SQ = 0.024                                    # 한 칸 실측 [m]  ← 자로 재 값!

objp = np.zeros((CB[0]*CB[1], 3), np.float32) # 보드 좌표계의 3D 점 (Z=0 평면)
objp[:, :2] = np.mgrid[0:CB[0], 0:CB[1]].T.reshape(-1, 2) * SQ
