# [60강. [실습] 도메인 랜덤화 학습 환경 구축]
- 모듈: ⑧ Sim2Real 및 가상 물리 시뮬레이션
- 한 줄 요약: 리셋 시점마다 물리·센서 파라미터 $\xi$를 분포에서 뽑아 적용하는 `DomainRandomizer`와, 성공률에 따라 랜덤화 폭을 조절하는 ADR 커리큘럼을 구현

## [핵심 개념]
- **도메인 랜덤화(DR)**
  - 파라미터 $\xi$(질량, 마찰, 게인, 지연, 노이즈 등)를 $\xi\sim p(\xi)$에서 샘플링
  - 목표: $\max_\pi\mathbb E_{\xi\sim p(\xi)}[R(\pi;\xi)]$ → 현실을 분포의 한 표본으로 만듦
  - 분포가 좁으면 현실을 못 덮고, 너무 넓으면 학습이 어렵거나 보수적 정책이 됨
- **리셋에 끼어드는 랜덤화**
  - 에피소드 시작(리셋)마다 해당 환경의 $\xi$만 재샘플 → 에피소드 내에서는 고정
  - 병렬 환경마다 서로 다른 $\xi$ → 한 배치가 곧 여러 도메인
- **설정표(yaml) 주도**
  - 파라미터별 `{dist, lo, hi, enabled}` → 축을 코드 수정 없이 켜고 끔
  - ablation(축 하나씩 끄기)으로 어떤 축이 gap에 기여하는지 분석 가능
- **재현성과 기록**
  - `np.random.default_rng(seed)`로 시드 고정
  - 에피소드별 $\xi$를 기록 → 실패 에피소드의 파라미터 영역 분석(62강)
- **ADR(Automatic Domain Randomization)**
  - 성공률이 높으면 폭 확대, 낮으면 축소하는 커리큘럼
  - 쉬운 분포에서 시작해 정책 능력에 맞춰 난이도 상승
  - 상·하한 임계(0.8 / 0.5) 사이는 유지 → 히스테리시스로 폭 진동 방지

## [파일별 내용]
- `01_dr.ipynb` — 원본 `dr.py`의 `DomainRandomizer` 클래스
  - `__init__(cfg, seed)`: 난수 생성기와 설정표 보관
  - `sample(env_ids)`: 활성 파라미터마다 `rng.uniform(lo, hi, len(env_ids))`로 환경 수만큼 값 생성 → `self.sim.set_param(name, env_ids, val)` 적용
  - `self.log_xi(env_ids, ...)`: 뽑은 $\xi$를 에피소드에 기록
  - 발췌 주의: `self.sim` 설정, `log_xi` 구현, `import numpy as np` 없음
  - 설정표의 `dist` 항목은 읽지 않고 항상 균등분포 사용
  - `c.enabled`처럼 속성 접근 → 주석의 dict 구조라면 `c["enabled"]` 또는 속성 접근 가능한 설정 객체 필요
- `02_adr.ipynb` — 원본 `adr.py`의 폭 조절 규칙
  - `recent_success_rate > 0.8` → `widen_all(cfg, step=0.05)`(각 축 폭 5%p 확대)
  - `recent_success_rate < 0.5` → `narrow_all(cfg, step=0.05)`(후퇴)
  - 빠진 맥락: `widen_all`/`narrow_all` 구현, 최근 성공률 집계 창, 호출 주기, 폭의 최대 한계

## [선수 지식·연결]
- 56강: DR·ADR 이론("계단" 커리큘럼)
- 59강: `ReachTask`의 `reset(env_ids)` → 여기서 랜덤화를 삽입하는 지점
- 59강 `proxy_sr`: DR 적용 후 gap이 줄었는지 판정 기준
- 62강: 기록된 $\xi$와 실물 로그로 System ID, 분포 재설정

## [실행 전 준비]
- Isaac Lab 환경 + NumPy
- 랜덤화 설정 yaml (파라미터별 범위)
- 파라미터를 환경 인덱스 단위로 바꿀 수 있는 시뮬 API

## [확인 포인트]
- 기대: DR 적용 시 `train_sr`은 다소 느려지지만 `proxy_sr`은 기준 학습보다 개선
- 흔한 실수: 매 스텝마다 $\xi$ 재샘플 → 물리 일관성 붕괴
- 흔한 실수: 시드·$\xi$ 미기록 → 실패 재현 불가
- 점검 질문
  - 질량·마찰 외에 "지연"과 "노이즈"를 랜덤화하는 이유는?
  - ADR에서 확대·축소 임계값을 같은 값으로 두면 어떤 현상이 생기는가?
  - 범위 `lo, hi`의 중심은 무엇을 기준으로 정해야 하는가?
