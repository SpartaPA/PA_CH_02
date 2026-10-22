# [67강. [실습] ONNX→TensorRT 변환·FP16/INT8 양자화]
- 모듈: ⑨ 에지 컴퓨팅 및 실시간 배포
- 한 줄 요약: 여러 모델을 ONNX로 내보내며 출력 정합을 검사하고(1구간), `trtexec`와 Python API로 FP32/FP16/INT8 TensorRT 엔진을 빌드(2구간)하는 변환 컨베이어 구성

## [핵심 개념]
- **변환 컨베이어**
  - 1구간: PyTorch → ONNX + 정합 검사
  - 2구간: ONNX → TensorRT 엔진(정밀도별)
  - 모든 모델에 같은 절차 적용 → 재현 가능한 배포 산출물
- **정합(parity) 검사**
  - 같은 입력 $n$개에 대해 $\max|y_{torch}-y_{onnx}|\le \text{atol}$ 확인
  - 변환 오류(지원 안 되는 연산, 잘못된 shape)를 엔진 빌드 전에 차단
- **TensorRT 엔진**
  - 대상 GPU에 맞춰 커널 선택·융합·메모리 계획을 미리 끝낸 직렬화 파일
  - GPU·TensorRT 버전에 종속 → 배포 기기에서 빌드하거나 동일 환경 필요
- **FP16**
  - 반정밀도로 연산 → 메모리·대역폭 절반, Tensor Core 활용
  - 대개 정확도 손실이 거의 없음
- **INT8 양자화**
  - $q=\text{round}(x/s)$, 복원 $\hat x=s\cdot q$, 범위는 $[-127,127]$로 클리핑
  - 스케일 $s$가 크면 해상도 손실, 작으면 클리핑 손실 → 균형 필요
  - **캘리브레이션**: 대표 입력을 흘려 각 텐서의 활성값 분포를 수집해 $s$ 결정
  - Entropy 캘리브레이터: 원 분포와 양자화 분포의 KL 발산을 최소화하는 임계 선택
  - 대표 데이터는 실제 배포 입력 분포를 반영해야 함(300~500 샘플)

## [파일별 내용]
- `01_export_all.ipynb` — 원본 `export_all.py`, 세 모델 공통 내보내기 루프
  - `MODELS`: `(name, model, dummy)` 튜플 목록(정의는 발췌에 없음)
  - `torch.onnx.export(..., opset_version=17)`
  - `check_parity(model, onnx_path, n=100, atol=1e-4)`: 100개 입력으로 오차 허용치 검사(구현은 발췌에 없음)
- `02_컨베이어_2구간_엔진_빌드.sh` — `trtexec` CLI 빌드
  - `--onnx=yolo.onnx --saveEngine=yolo_fp32.engine`: 기본(FP32) 엔진
  - `--fp16`: FP16 허용 엔진
  - INT8은 캘리브레이터가 필요해 Python API로 분리
- `03_컨베이어_2구간_엔진_빌드.ipynb` — INT8 캘리브레이터 핵심
  - `class Calibrator(trt.IInt8EntropyCalibrator2)`: `get_batch(names)`가 다음 대표 배치 반환
  - 빌더 설정: `config.set_flag(trt.BuilderFlag.INT8)`, `config.int8_calibrator = ...`
  - 빠진 맥락: `__init__`(부모 생성자 호출, `data_iter` 준비), `get_batch_size()`, 캐시 읽기/쓰기(`read_calibration_cache`/`write_calibration_cache`)
  - 주의: 실제 `get_batch`는 GPU에 복사한 버퍼의 **디바이스 포인터(int) 목록**을 반환해야 하며, 데이터 소진 시 `None` 반환
  - 주의: 최신 TensorRT 버전은 암시적 INT8 캘리브레이션을 비권장으로 두고 명시적 양자화(Q/DQ 노드)를 권장 → 설치 버전 문서 확인

## [선수 지식·연결]
- 63강: ONNX 내보내기, 정합 규율, 고정 shape
- 64강: TensorRT·양자화 이론
- 29강(④ YOLO): 변환 대상 `yolo` 모델
- 68강: 정밀도별 엔진의 지연·메모리·전력 비교
- 69강: 엔진 파일(+결정서·해시)을 배포 패키지 `engines/`에 포함

## [실행 전 준비]
- NVIDIA GPU(또는 Jetson) + TensorRT, `trtexec`(보통 `/usr/src/tensorrt/bin/`)
- Python `tensorrt`, `pycuda` 또는 `cuda-python`(캘리브레이션 버퍼 복사)
- 대표 입력 데이터셋(300~500 샘플)

## [확인 포인트]
- 기대: FP32 → FP16 → INT8 순으로 지연 감소, 정확도는 FP16 거의 동일·INT8 소폭 하락 가능
- 흔한 실수: 정합 검사 없이 엔진 빌드 → 원인 구분 불가
- 흔한 실수: 캘리브레이션 데이터를 학습 데이터 일부나 무작위 노이즈로 대체 → INT8 정확도 급락
- 점검 질문
  - FP16 엔진의 출력 오차 허용치는 FP32 정합 때와 같아야 하는가?
  - 개발 PC에서 빌드한 엔진을 Jetson에 복사하면 왜 실패할 수 있는가?
  - INT8 정확도가 떨어질 때 어떤 레이어를 FP16으로 남길지 어떻게 정하는가?
