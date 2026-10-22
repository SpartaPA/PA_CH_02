# [53강. [실습] 정책 성능(Success Rate·Smoothness) 검증]
- 모듈: ⑦ 로봇 모방학습 및 정책 최적화
- 한 줄 요약: `policy(obs) -> action` 규약만 맞추면 BC든 Diffusion Policy든 같은 조건으로 롤아웃·채점·리포트를 내는 공용 평가 패키지 설계

## [핵심 개념]
- **인터페이스 통일** → 평가기는 정책 내부를 모름, `policy(obs) -> action`만 호출 → 정책 간 공정 비교
- **성공 판정 4조건** → 도달 반경, 시간 한도, 충돌 없음, 관절 한계 내 (51강 3조건 + 충돌)
- **성공률과 Wilson 신뢰구간** → 이항 비율 $\hat p$, 표본 $n$, $z\approx1.96$(95%)
  - $\dfrac{\hat p+\frac{z^2}{2n}\pm z\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}}}{1+\frac{z^2}{n}}$
  - $\hat p$가 0·1 근처이거나 $n$이 작을 때 정규근사보다 안정
- **Smoothness(jerk)** → jerk $j=\dddot q$, 이산 시간에서 3차 차분 $j_t\approx\frac{q_{t+1}-3q_t+3q_{t-1}-q_{t-2}}{\Delta t^3}$, 지표는 RMS
  - 성공해도 덜컥거리는 정책은 실물에서 기계 부담·추적 오차 유발
- **행동 변화량** → $\|a_t-a_{t-1}\|$, 명령 떨림 측정(리시딩 호라이즌 재생성 시 경계 점프 확인)
- **경로 길이비** → 실제 경로 길이 / 최단(직선) 거리, 우회 정도
- **조건 격자 × 반복 × 시드** → 분포 전체를 덮는 체계적 평가, 실패 위치 지도화
- **재현성** → 커밋 해시·설정을 결과와 함께 저장

## [파일별 내용]
- `01_평가기_정책을_꽂으면_리포트가_나온다.ipynb` — `policy_eval/` 패키지 구성(주석만, 구현 없음)
  - `interface`: `policy(obs) -> action` 규약
  - `runner`: 조건 격자 × 반복 × 시드 롤아웃(45강 `bench_runner`의 정책판)
  - `judge`: 성공 4조건
  - `metrics`: success(+Wilson CI), 도달 시간, jerk RMS, 행동 변화량, 경로 길이비
  - `report`: 대시보드 그림 + yaml 결과(커밋 해시·설정 포함)
  - 주의: 52강 Diffusion Policy는 시퀀스를 내므로 내부 버퍼로 한 스텝씩 꺼내는 어댑터가 필요

## [선수 지식·연결]
- 51강 `rollout_eval.py`(1차 버전)의 확장, 45강 `bench_runner`와 같은 구조
- 15강 Quintic 궤적: 가속도·jerk가 작은 궤적의 의미
- 47·51·52강 정책이 평가 대상, 54강 DAgger 라운드별 `eval_report`로 재사용

## [실행 전 준비]
- `numpy`, `matplotlib`, `pyyaml`, `torch`(정책 로드), 2링크 시뮬레이터
- git 저장소(커밋 해시 기록용)

## [확인 포인트]
- 기대 결과: 정책별 성공률±Wilson CI, jerk RMS 등 지표표, 대시보드 그림, yaml 결과 파일
- 흔한 실수: 정책마다 다른 시드·조건으로 비교, CI 없이 성공률 차이 단정, 시간 간격 $\Delta t$ 무시한 jerk 계산
- 점검 질문
  - 성공률 18/20과 17/20은 Wilson CI로 보면 구분되는가?
  - Diffusion Policy가 성공률은 높고 jerk가 크다면 어디를 의심하는가?
  - 평가 결과에 커밋 해시가 없으면 어떤 문제가 생기는가?
