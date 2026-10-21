# [CH2 Physical AI] 25강. YOLO 계열 객체 검출 파이프라인
# 절: Ultralytics로 추론 — 다섯 줄
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

from ultralytics import YOLO
model = YOLO("yolov8n.pt")          # n(ano)~x: 크기/정확도 트레이드오프
results = model(frame, conf=0.5)     # ndarray 입력 (16강의 그 배열)
for b in results[0].boxes:
    xyxy, cls, conf = b.xyxy[0], int(b.cls), float(b.conf)
