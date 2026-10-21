# [CH2 Physical AI] 68강. [실습] 추론 지연(P50/P99)·메모리/전력 프로파일링
# 절: 1. 지연 프로파일러 — 구간 분해와 분포
# 원본 경로: profiler.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# profiler.py — 66강 예산표의 측정점을 코드로
with Timer("capture"):  frame = cam.read()
with Timer("pre"):      x = preprocess(frame)
with Timer("infer"):    y = engine.run(x)
with Timer("post"):     out = postprocess(y)
# Timer는 사전 할당된 배열에 기록 (측정이 지연을 만들지 않게!)
