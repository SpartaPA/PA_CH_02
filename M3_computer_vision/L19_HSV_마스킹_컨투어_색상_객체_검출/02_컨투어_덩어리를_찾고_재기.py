# [CH2 Physical AI] 19강. [실습] HSV 마스킹·컨투어 색상 객체 검출
# 절: 2. 컨투어 — 덩어리를 찾고 재기
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

def detect(mask, min_area=300):
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best = None
    for c in cnts:
        area = cv2.contourArea(c)
        if area < min_area:
            continue                          # ① 면적 필터: 점 노이즈 제거
        peri = cv2.arcLength(c, True)
        circularity = 4 * np.pi * area / (peri * peri + 1e-9)
        if circularity < 0.6:
            continue                          # ② 형상 필터: 공이면 원형도
        if best is None or area > best[0]:
            best = (area, c)
    if best is None:
        return None
    M = cv2.moments(best[1])                  # ③ 모멘트로 중심
    cx, cy = M["m10"] / M["m00"], M["m01"] / M["m00"]
    x, y, w, h = cv2.boundingRect(best[1])
    return {"center": (cx, cy), "bbox": (x, y, w, h), "area": best[0]}
