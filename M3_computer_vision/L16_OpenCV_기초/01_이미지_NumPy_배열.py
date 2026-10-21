# [CH2 Physical AI] 16강. OpenCV 기초 (입출력·HSV·필터링·모폴로지)
# 절: 1. 이미지 = NumPy 배열
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

import cv2
import numpy as np

img = cv2.imread("scene.jpg")        # ndarray로 로드
print(img.shape, img.dtype)          # (480, 640, 3) uint8
