# [CH2 Physical AI] 67강. [실습] ONNX→TensorRT 변환·FP16/INT8 양자화
# 절: 1. 컨베이어 1구간 — 내보내기와 정합
# 원본 경로: export_all.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# export_all.py — 세 모델 공통 절차
for name, model, dummy in MODELS:
    torch.onnx.export(model, dummy, f"{name}.onnx", opset_version=17)
    check_parity(model, f"{name}.onnx", n=100, atol=1e-4)   # 63강 규율
