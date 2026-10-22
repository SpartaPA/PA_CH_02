# [51강. [실습] MLP/CNN/Transformer BC 정책 학습]
- 모듈: ⑦ 로봇 모방학습 및 정책 최적화
- 한 줄 요약: 아키텍처만 바꿔 끼우는 공용 BC 학습기를 만들고, MLP·CNN·Transformer 정책을 같은 롤아웃 평가 프로토콜로 비교

## [핵심 개념]
- **공용 학습기** → 데이터·손실·옵티마이저·로깅·체크포인트는 고정, 모델만 교체 → 공정한 아키텍처 비교
- **BC 손실** → $\mathcal L=\frac1B\sum\|\pi_\theta(o_i)-a_i\|^2$
- **AdamW** → Adam + 가중치 감쇠 분리(decoupled weight decay)
- **동결 분할(frozen split)** → train/val을 한 번 정해 고정 → 실험 간 비교 가능, 정규화 통계도 train 기준
- **검증 기반 체크포인트** → val MSE 최소 모델 저장(과적합 직전)
  - 단, val MSE가 낮다고 롤아웃 성공률이 높다는 보장 없음 → 롤아웃 평가 별도 필요
- **아키텍처별 역할**
  - MLP: 저차원 상태 관측(6차원)
  - CNN: 이미지 관측 → 합성곱 인코더로 특징 추출 후 관절 상태와 결합
  - Transformer: 관측 이력 등 시퀀스 입력을 attention으로 처리(이 폴더엔 코드 없음)
- **합성곱 출력 크기** → $\lfloor (W-k)/s\rfloor+1$ (패딩 0 기준)
- **롤아웃 평가** → 학습 데이터 지표(MSE)가 아니라 실제 폐루프 실행 결과로 판정, 시드 반복으로 분산 보고

## [파일별 내용]
- `01_train_bc.ipynb` — `train_bc.py`의 `train(model, cfg)`
  - `DemoDataset("demos_clean.hdf5", split="train")`: 50강 산출물, 동결 분할
  - `DataLoader(batch_size=256, shuffle=True)`, `AdamW(lr=cfg.lr)`
  - 에포크마다 `evaluate_mse(model, split="val")` → `save_if_best` → `log`(CSV, 학습 곡선 원천)
  - 빠진 맥락: `DemoDataset`, `evaluate_mse`, `save_if_best`, `log`, `cfg` 정의와 import
- `02_②_CNN_이미지_관측_의사코드.txt` — 작은 CNN 인코더 구조
  - `Conv(3→32,k4,s2) → Conv(32→64,k4,s2) → Conv(64→64,k3,s1) → flatten`
  - `concat[관절 상태 4]`(관절각·관절속도) → MLP 머리
  - 이미지 해상도·활성함수는 명시 없음
- `03_rollout_eval.ipynb` — `rollout_eval.py` 프로토콜(주석만, 53강에서 확장)
  - 시작 조건: 물체 위치 10×10 격자(훈련 5×5보다 촘촘 → 보간 능력 측정)
  - 성공: 반경 0.02 m 내 도달, 시간 한도 10 s, 관절 한계 위반 없음
  - 보고: 시드 3개 성공률 평균±표준편차, 성공 지도, 평균 도달 시간

## [선수 지식·연결]
- 47강: MLP 정책과 MSE 손실, 50강: `demos_clean.hdf5`·정규화 통계
- 16·25강: 합성곱·백본(CNN 인코더의 원형)
- 52강: 같은 데이터에서 Diffusion Policy와 비교, 53강: 평가기 확장, 54강: DAgger 루프에서 `train_bc` 재사용

## [실행 전 준비]
- `torch`, `h5py`, `numpy`
- 50강 `demos_clean.hdf5`, 롤아웃용 2링크 시뮬레이터
- GPU 권장(CNN·Transformer)

## [확인 포인트]
- 기대 결과: 에포크별 train/val 손실 CSV, 최적 체크포인트, 아키텍처별 성공률 비교표와 성공 지도
- 흔한 실수: val로 하이퍼파라미터를 고른 뒤 같은 val 결과를 최종 성능으로 보고, 시드 1개로 결론
- 점검 질문
  - val MSE가 가장 낮은 모델이 성공률도 가장 높았는가? 아니라면 왜?
  - 성공 지도에서 실패가 몰린 영역은 훈련 격자 5×5와 어떤 관계인가?
  - CNN 인코더 입력 해상도를 바꾸면 flatten 차원은 어떻게 바뀌는가?
