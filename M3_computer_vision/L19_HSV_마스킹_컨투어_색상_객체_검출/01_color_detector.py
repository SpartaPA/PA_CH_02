# [CH2 Physical AI] 19강. [실습] HSV 마스킹·컨투어 색상 객체 검출
# 절: 1. 전처리 — 16강의 복습을 코드로
# 원본 경로: src/color_detector.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/color_detector.py
import cv2
import numpy as np

def make_mask(frame_bgr, lo, hi, lo2=None, hi2=None):
    """블러 → HSV → inRange(범위 1~2개) → 열림 → 닫힘."""
    blur = cv2.GaussianBlur(frame_bgr, (5, 5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lo, hi)
    if lo2 is not None:                       # 빨강: H가 감기는 두 조각
        mask |= cv2.inRange(hsv, lo2, hi2)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    return mask
