# [6강. [실습] ADC·엔코더 센서 인터페이스]
- 모듈: ① 임베디드 제어 기초
- 한 줄 요약: 가변저항을 ADC로 읽고 UART로 로깅하며 EMA로 다듬은 뒤, 타이머 엔코더 모드로 모터 속도(RPM)를 측정해 개루프 구동과 한데 묶음

## [핵심 개념]
- ADC(12비트)
  - 원값 0~4095 ↔ 0~$V_{ref}$(3.3 V): $V=\text{raw}\cdot 3.3/4095$
  - 폴링 변환: 시작 → 완료 대기 → 값 읽기
- UART 로깅
  - `printf`를 UART로 리다이렉트(`_write` 재정의) → PC 시리얼 터미널·CSV로 관찰
  - 블로킹 송신은 시간 소모 → 제어 ISR 안에서는 금지, 메인 루프에서만
- EMA(지수이동평균) 필터
  - $y_k=\alpha x_k+(1-\alpha)y_{k-1}$, 코드는 $\alpha=0.2$
  - $\alpha$ 작을수록 매끄럽지만 지연 증가(1차 저역통과 필터)
- 쿼드러처 엔코더
  - A/B 두 채널의 90° 위상차로 회전 방향 판별
  - STM32 타이머 엔코더 모드가 하드웨어로 카운트 증감
  - 4체배 시 CPR = 슬롯 수 × 4 × 감속비(코드는 출력축 기준 1320)
- 속도 계산
  - 고정 주기 $\Delta t$의 카운트 차분: $\text{RPM}=\frac{\Delta N}{\text{CPR}}\cdot\frac{60}{\Delta t}$
  - 부호 있는 정수 차분 → 카운터 랩어라운드도 차분 결과로 자연 처리(카운터 비트 폭과 형 변환 일치 전제)

## [파일별 내용]
- `01_설정과_코드_가변저항_읽기.c` — `adc_read_raw()`(0~4095), `adc_read_volt()`(V 환산)
  - `HAL_ADC_PollForConversion(&hadc1, 10)`: 최대 10 ms 대기
- `02_UART_로깅_측정을_눈으로.c` — `_write()`를 재정의해 `printf` 출력을 `huart2`로 전송
  - newlib 기반 GCC 툴체인(STM32CubeIDE) 전제
- `03_필터_떨리는_값_다듬기.c` — `ema(float x)`, 내부 `static float y` 상태
  - 함수 하나 = 필터 하나 → 신호마다 별도 함수/상태 필요
  - 초기값 0에서 출발 → 첫 몇 샘플은 실제보다 작게 나옴
- `04_STM32_타이머_엔코더_모드.c` — `HAL_TIM_Encoder_Start(&htim2, TIM_CHANNEL_ALL)` + `encoder_count()`
  - TIM2 카운터를 `int32_t`로 읽어 방향에 따라 증감
- `05_속도_계산.c` — TIM7 주기 콜백(10 ms)에서 속도 계산
  - `CPR 1320.0f`, `diff = now - prev`, `rev_per_s = diff / CPR / 0.010f`
  - `volatile float speed_rpm`: ISR이 쓰고 메인 루프가 읽음
  - 발췌: `ema_speed()`는 정의가 보이지 않음 → 03의 `ema`와 같은 형태의 속도 전용 필터로 별도 작성 필요
- `06_통합_오늘의_결과물.c` — 메인 루프(20 Hz)
  - 가변저항 → 0~1 → `motor_write(knob)`로 듀티 직접 지정(개루프)
  - `printf("%lu, %.2f, %.1f")`: 시간(ms)·노브·RPM CSV 로그
  - `%f` 출력에는 newlib-nano float printf 옵션 활성화 필요

## [선수 지식·연결]
- 4강 레지스터/HAL, 5강 `motor_write`
- 7강: `speed_rpm` 측정을 `measure_speed_rpm()`으로 묶고 PID 되먹임에 사용, 공유 변수 `volatile`
- 7강 위치 제어: `encoder_count()`를 각도로 환산해 재사용

## [실행 전 준비]
- CubeMX: ADC1(가변저항 입력 핀), USART2, TIM2 Encoder Mode(A/B), TIM7 10 ms 주기 인터럽트
- 엔코더 달린 감속 DC 모터, 드라이버, 가변저항, USB 시리얼 터미널

## [확인 포인트]
- 기대 결과: 노브를 돌리면 모터 속도가 변하고, 로그에 노브값과 RPM이 함께 증감
- 흔한 실수
  - CPR을 모터축 기준으로 잡아 출력축 RPM이 감속비만큼 틀림
  - 엔코더 A/B 결선이 반대면 부호 반전
- 점검 질문
  - $\Delta t$를 10 ms에서 1 ms로 줄이면 저속에서 속도 분해능은 어떻게 되는가?
  - EMA의 $\alpha$를 0.05로 낮추면 로그 곡선의 지연이 얼마나 늘어나는가?
