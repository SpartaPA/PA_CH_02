# [CH2 Physical AI] 63강. ONNXRuntime 추론 최적화 (Graph Optimization·Operator Fusion)
# 절: 3. ONNXRuntime — 실행 공급자(EP)라는 설계
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

import onnxruntime as ort
sess = ort.InferenceSession("policy.onnx",
        providers=["TensorrtExecutionProvider",      # 우선순위대로 시도
                   "CUDAExecutionProvider",
                   "CPUExecutionProvider"])           # 폴백
action = sess.run(None, {"obs": obs_np})[0]
