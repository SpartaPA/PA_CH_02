# [7강. [실습] PID 펌웨어 목표값 추종 (속도/위치)]
- 모듈: ① 임베디드 제어 기초
- 한 줄 요약: 3강의 이산 PID를 재사용 가능한 C 모듈로 완성하고, 타이머 ISR에서 측정(6강)–PID–구동(5강)을 조립해 목표 속도·위치를 추종하는 펌웨어 작성

## [핵심 개념]
- 고정 주기 제어 루프
  - 타이머 인터럽트로 $dt$를 일정하게 유지(메인 루프의 `HAL_Delay`는 주기가 흔들림)
  - ISR: 측정 → 계산 → 출력만, 로깅·통신은 메인 루프
- `volatile`
  - ISR과 메인 루프가 공유하는 변수는 컴파일러가 레지스터에 캐시하지 못하게 함
  - `volatile`은 원자성 보장이 아님 → Cortex-M에서 32비트 정렬 `float` 단일 읽기/쓰기는 원자적, 여러 변수를 묶어 읽을 땐 일관성 주의
- 개선된 PID(3강 심화 반영)
  - 측정값 미분: $D=-K_d\,\frac{y_k-y_{k-1}}{dt}$ → 목표값 계단 시 derivative kick 제거
  - 미분 EMA 필터: $d_k=d_{k-1}+\alpha_d(d_{raw}-d_{k-1})$, $\alpha_d$ 0.1~0.3
  - 조건부 적분(anti-windup): 포화 방향으로 밀고 있을 때 적분 동결
  - 최종 출력 포화 $[u_{min},u_{max}]$
- 속도 제어 vs 위치 제어
  - 속도: 측정 = 엔코더 증분 기반 RPM
  - 위치: 측정 = 누적 카운트 → 각도 $\theta=N\cdot 360/\text{CPR}$
  - 위치 루프는 속도와 다른 플랜트(적분기 하나 추가) → 이득을 별도 튜닝

## [파일별 내용]
- `01_공유_변수와_volatile.c` — 전역 `g_target_rpm`(메인→ISR), `g_speed_rpm`·`g_duty`(ISR→메인, 로깅용)
- `02_PID_모듈_구현.c` — `PID` 구조체와 `pid_step(PID *c, float ref, float meas)`, `pid_reset()`
  - 구조체: 이득, `dt`, `out_min/out_max`, `integral`, `meas_prev`, `d_filt`, `d_alpha`
  - 3강과 달리 `dt`를 구조체에 보관(인자에서 제거)
  - 계산 순서: 오차 → 측정값 미분+필터 → 잠정 출력 → `saturating` 판정 후 적분 → 클램프
  - `pid_reset()`이 `meas_prev = 0` → 측정값이 0이 아닌 상태에서 리셋하면 첫 주기 D 항이 튐(필터로 완화)
- `03_ISR에서_조립.c` — 전역 `g_pid` 초기화와 TIM7 콜백
  - `dt=0.001f`(1 kHz), 출력 ±1(=`motor_write` 범위), `d_alpha=0.2f`
  - `Kp=Ki=Kd=0`으로 시작 → 튜닝하며 값을 올리는 출발점
  - 콜백: `measure_speed_rpm()` → `pid_step()` → `motor_write()`
  - 발췌: `measure_speed_rpm()`은 6강 `05_속도_계산.c`를 함수로 묶은 것(본문에 정의 없음), 6강의 TIM7 10 ms 설정과 달리 1 ms 주기로 맞춰야 함
- `04_위치_제어로_확장.c` — 두 줄 발췌
  - `angle_deg = encoder_count() * 360.0f / CPR`
  - `pid_step(&g_pid_pos, g_target_deg, angle_deg)`
  - `g_pid_pos`, `g_target_deg` 선언은 생략 → 속도용과 별도 `PID` 인스턴스

## [선수 지식·연결]
- 3강: 이산 PID, anti-windup 원리
- 5강: `motor_write()`, 6강: 엔코더 카운트·RPM 계산·EMA
- 8강: 여기의 `volatile` 전역(`g_target_rpm`, `g_speed_rpm`, `g_duty`)을 micro-ROS 콜백이 그대로 읽고 씀
- 15강: 관절 PID + 중력 보상으로 같은 구조를 로봇팔에 적용

## [실행 전 준비]
- 5·6강 프로젝트(PWM, 엔코더 모드, UART 로깅)에 이어서 작성
- TIM7을 1 kHz 업데이트 인터럽트로 설정, NVIC 활성화
- 엔코더 달린 DC 모터 + 드라이버

## [확인 포인트]
- 기대 결과: 목표 RPM 계단 변경 시 측정 RPM이 오버슈트 작게 따라가고 정상상태 오차가 사라짐
- 튜닝 절차 예: $K_p$만 올려 반응 확인 → 진동 시 $K_d$ → 정상상태 오차를 $K_i$로 제거
- 흔한 실수
  - ISR 안에서 `printf` 호출 → 주기 붕괴
  - 속도 측정 주기와 제어 주기 불일치 → 계수 의미 왜곡
- 점검 질문
  - 모터를 손으로 잡아 포화시킨 뒤 놓았을 때 anti-windup 유무에 따라 응답이 어떻게 다른가?
  - 위치 제어에서 $K_i$를 크게 하면 왜 진동이 쉽게 생기는가?
