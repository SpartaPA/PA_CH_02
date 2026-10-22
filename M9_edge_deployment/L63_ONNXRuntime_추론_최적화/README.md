# [63강. ONNXRuntime 추론 최적화 (Graph Optimization·Operator Fusion)]
- 모듈: ⑨ 에지 컴퓨팅 및 실시간 배포
- 한 줄 요약: PyTorch 모델을 고정 shape ONNX 그래프로 내보내고, ONNXRuntime의 그래프 최적화와 실행 공급자(EP) 우선순위로 하드웨어에 맞춰 추론

## [핵심 개념]
- **ONNX = 모델의 표준 도면**
  - 연산자(노드)와 텐서(엣지)로 이루어진 프레임워크 독립 계산 그래프
  - 학습 프레임워크와 추론 엔진을 분리 → 같은 파일을 CPU/GPU/TensorRT에서 실행
  - `opset` 버전이 사용 가능한 연산자 집합을 결정
- **고정 shape의 이점**
  - `dynamic_axes=None` → 모든 차원이 상수
  - 메모리 계획·커널 선택·연산자 융합을 빌드 시점에 확정 가능
  - 배치 크기가 바뀌는 용도라면 동적 축이 필요하지만 최적화 여지 감소
- **그래프 최적화**
  - 상수 접기: 입력과 무관한 부분 계산을 미리 수행
  - 연산자 융합: Conv+BN+ReLU 등을 한 커널로 → 메모리 왕복·커널 호출 감소
  - BN 접기: $y=\gamma\frac{Wx+b-\mu}{\sigma}+\beta$ → $W'=\frac{\gamma}{\sigma}W,\;b'=\frac{\gamma}{\sigma}(b-\mu)+\beta$
- **실행 공급자(EP)**
  - 하드웨어별 백엔드: TensorRT / CUDA / CPU
  - `providers` 리스트 순서 = 우선순위, 지원 안 되는 노드는 다음 EP로 폴백
  - CPU EP를 마지막에 두어 항상 실행 가능하게 보장
- **워밍업**
  - 첫 실행은 초기화·엔진 빌드·메모리 할당으로 느림 → 측정·서비스 전 N회 더미 실행(69강 노드에서 사용)
- **정합 확인**
  - 변환 전후 출력 차이를 허용치(`atol`) 내로 검증(67강 `check_parity`)

## [파일별 내용]
- `01_ONNX_모델의_표준_도면.ipynb` — 내보내기 호출
  - `torch.onnx.export(model, dummy_input, "policy.onnx", input_names=["obs"], output_names=["action"], dynamic_axes=None)`
  - `input_names`/`output_names`: 추론 시 딕셔너리 키(`"obs"`)와 결과 이름 고정
  - `dummy_input`: 실제 입력과 같은 shape·dtype → 이 shape가 그대로 고정됨
  - 빠진 맥락: `model` 정의·가중치 로드, `model.eval()`, `opset_version` 지정
- `02_ONNXRuntime_실행_공급자_EP_라는_설계.ipynb` — 세션 생성과 추론
  - `ort.InferenceSession("policy.onnx", providers=[TensorRT, CUDA, CPU])`
  - `sess.run(None, {"obs": obs_np})[0]`: `None` = 모든 출력 반환, `[0]` = 첫 출력(`action`)
  - `obs_np`: NumPy 배열, dtype은 내보낼 때와 동일(보통 `float32`)
  - 빠진 맥락: `SessionOptions`의 `graph_optimization_level` 설정, 최적화 그래프 저장 옵션

## [선수 지식·연결]
- 61강: `dr_policy.onnx` 내보내기를 미리 사용
- 64강: TensorRT 이론 → 67강 엔진 빌드 실습
- 66강: 지연 예산 → 68강 프로파일링
- 69강: 워밍업·폴백 규율을 최종 추론 노드에 통합

## [실행 전 준비]
- `torch`, `onnx`, `onnxruntime` 또는 `onnxruntime-gpu`
- GPU EP 사용 시 버전이 맞는 CUDA/cuDNN/TensorRT
- `ort.get_available_providers()`로 사용 가능한 EP 확인

## [확인 포인트]
- 기대: 지원 EP가 있으면 상위 EP로 실행, 없으면 경고 후 CPU로 폴백
- 흔한 실수: `onnxruntime`(CPU 전용) 설치 상태에서 CUDA EP 지정 → 조용히 CPU로 실행
- 흔한 실수: 입력 dtype `float64` 전달 → 타입 오류
- 점검 질문
  - 고정 shape로 내보낸 모델에 배치 2를 넣으면 어떻게 되는가?
  - `sess.get_providers()`로 실제 사용 중인 EP를 확인했는가?
  - 연산자 융합이 정확도를 바꿀 수 있는 경우는?
