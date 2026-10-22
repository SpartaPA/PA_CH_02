# [55강. Isaac Sim/Isaac Lab 태스크 구성 (USD Asset·Sensor)]
- 모듈: ⑧ Sim2Real 및 가상 물리 시뮬레이션
- 한 줄 요약: GPU 병렬 시뮬레이션이 왜 필요한지 이해하고, 수천 개 환경을 한 배치로 돌리는 `reset`/`step` 인터페이스 감각을 익힘

## [핵심 개념]
- **병렬성 = 도구의 존재 이유**
  - 강화학습은 수백만~수억 스텝의 상호작용이 필요 → 단일 환경 실시간 시뮬로는 불가능
  - Isaac Lab은 USD 장면을 GPU에서 `num_envs`개 복제해 한 번에 물리 계산
  - 처리량 ≈ `num_envs` × 스텝 속도, 데이터가 GPU 텐서로 머물러 CPU↔GPU 복사 최소화
- **배치 텐서 인터페이스**
  - 관측 `obs`: `(num_envs, obs_dim)`, 행동 `act`: `(num_envs, act_dim)`
  - 정책도 배치 입력을 한 번에 처리 → 환경 루프 대신 텐서 연산
- **Gym 스타일 루프**
  - `reset()` → 초기 관측, `step(act)` → `(obs, reward, done, info)`
  - MDP $(S, A, P, R, \gamma)$의 상호작용을 코드로 옮긴 형태
  - 목표: 기대 누적 보상 $\mathbb E\left[\sum_t \gamma^t r_t\right]$ 최대화
- **USD Asset·Sensor**
  - USD(Universal Scene Description): 로봇·물체·조명·센서를 계층 장면으로 기술하는 포맷
  - 센서(카메라·관절 상태 등)도 장면의 일부로 붙여 관측 생성
- **관측 규율(Sim2Real 대비)**
  - 관측에는 실물에서도 얻을 수 있는 값만 사용(시뮬 전용 정답 상태 금지)
  - 59강 `ReachTask` 관측 설계의 근거

## [파일별 내용]
- `01_병렬성_이_도구의_존재_이유.ipynb` — Isaac Lab 스타일 **의사코드**(실행 불가)
  - `TaskEnv(num_envs=4096, device="cuda")`: 4096개 환경을 GPU에 생성
  - `env.reset()` → `(4096, obs_dim)` 관측
  - `for step in range(horizon)`: `policy(obs)`로 배치 행동 산출 → `env.step(act)`
  - 주의: `TaskEnv`, `policy`, `horizon`은 정의되지 않은 가상 이름
  - 실제 Isaac Lab에서는 `ManagerBasedRLEnv`/`DirectRLEnv` 등 설정 클래스로 환경 구성, `done`은 `terminated`/`truncated`로 분리되는 경우가 많음
  - 개별 환경 종료 시 해당 환경만 자동 리셋되는 구조(59강 `reset(env_ids)`로 이어짐)

## [선수 지식·연결]
- ⑦ 모방학습(46~54강): 정책 $\pi(o)$ 개념, 관측·행동 정규화
- 56강: 도메인 랜덤화 이론 → 60강 구현
- 59강: 이 인터페이스로 실제 태스크(`ReachTask`) 정의
- 61강: 학습된 정책을 실물로 내보냄

## [실행 전 준비]
- NVIDIA GPU(RTX급) + Isaac Sim / Isaac Lab 설치
- PyTorch(CUDA), Python 환경은 Isaac Lab 제공 스크립트 기준
- 이 노트북 자체는 개념 코드라 그대로 실행되지 않음

## [확인 포인트]
- 기대: `num_envs`를 늘려도 스텝당 시간은 완만히 증가 → 초당 총 샘플 수 급증
- 흔한 실수: 정책을 환경마다 for문으로 호출 → 병렬성 상실
- 흔한 실수: 관측 텐서를 매 스텝 CPU로 복사해 처리량 저하
- 점검 질문
  - `obs`의 첫 번째 축은 무엇을 뜻하는가?
  - 시뮬에서만 알 수 있는 값(물체 정확한 질량 등)을 관측에 넣으면 실물 배포에서 무슨 문제가 생기는가?
  - `num_envs`가 GPU 메모리에 의해 제한되는 이유는?
