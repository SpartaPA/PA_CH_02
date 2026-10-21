# [CH2 Physical AI] 63강. ONNXRuntime 추론 최적화 (Graph Optimization·Operator Fusion)
# 절: 1. ONNX — 모델의 "표준 도면"
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

torch.onnx.export(model, dummy_input, "policy.onnx",
                  input_names=["obs"], output_names=["action"],
                  dynamic_axes=None)          # 고정 shape가 최적화에 유리 (아래)
