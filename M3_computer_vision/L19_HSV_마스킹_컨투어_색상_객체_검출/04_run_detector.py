# [CH2 Physical AI] 19강. [실습] HSV 마스킹·컨투어 색상 객체 검출
# 절: 3. 통합 루프와 성능 측정
# 원본 경로: scripts/run_detector.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# scripts/run_detector.py
det = ColorDetector(config["red"])           # make_mask + detect + EMA를 클래스로
cap = cv2.VideoCapture(0)
t0, n = time.time(), 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    r = det.step(frame)
    if r:
        cv2.circle(frame, (int(r["cx"]), int(r["cy"])), 6, (0, 255, 0), -1)
        cv2.rectangle(frame, r["bbox"][:2],
                      (r["bbox"][0]+r["bbox"][2], r["bbox"][1]+r["bbox"][3]),
                      (0, 255, 0), 2)
    n += 1
    if n % 30 == 0:
        print(f"FPS: {30 / (time.time() - t0):.1f}"); t0 = time.time()
    cv2.imshow("detector", frame)
    if cv2.waitKey(1) == 27:
        break
