# [5강. [실습] GPIO·타이머·PWM 액추에이터 구동 (DC/서보)]
- 모듈: ① 임베디드 제어 기초
- 한 줄 요약: 빌드–플래시–관찰 사이클을 익히고, 버튼 입력을 폴링·인터럽트로 처리한 뒤, 타이머 PWM으로 서보 각도와 DC 모터 속도·방향을 구동

## [핵심 개념]
- 빌드–플래시–관찰 사이클: CubeMX 설정 → 코드 → 빌드 → ST-LINK 플래시 → LED/계측으로 확인
- CubeMX 생성 코드 규칙: `/* USER CODE BEGIN ... */`~`END` 구역 안에만 작성(재생성 시 보존)
- 입력 처리 방식
  - 폴링: 메인 루프가 계속 핀을 읽음 → 단순, CPU 점유·놓침 위험
  - 인터럽트(EXTI): 엣지 발생 시 콜백 → 즉각 반응, ISR은 짧게
  - 버튼 채터링: 기계 접점의 떨림으로 여러 번 트리거 가능(디바운스 필요)
- PWM
  - 듀티비 $D=\text{CCR}/(\text{ARR}+1)$ → 모터 평균 전압 $\approx D\cdot V_{supply}$
  - 주파수: 서보 50 Hz(주기 20 ms), DC 모터 약 21 kHz(가청 대역 밖)
- 서보: 펄스 폭으로 각도 지령 → 코드는 0~180° ↔ 1000~2000 µs 선형 매핑
- DC 모터 + H-브리지 드라이버: 방향 핀(GPIO) + 크기(PWM 듀티)로 부호 있는 명령 $u\in[-1,1]$ 구현

## [파일별 내용]
- `01_빌드_플래시_관찰_사이클.c` — `while(1)`에서 `HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5)` + `HAL_Delay(500)`
  - LD2 LED가 1 s 주기(500 ms 켜짐/꺼짐)로 깜빡임 → 툴체인 동작 확인용 "Hello World"
- `02_폴링_방식.c` — PC13 버튼을 계속 읽어 눌림(`GPIO_PIN_RESET`, Low)이면 PA5 LED 켬
  - 버튼이 active-low(누르면 Low)라는 전제
- `03_인터럽트_방식.c` — `HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)`
  - `GPIO_PIN_13`이면 LED 토글만 하고 즉시 리턴(ISR은 짧게)
  - 전제: CubeMX에서 PC13을 EXTI 모드로, NVIC 인터럽트 활성화
- `04_코드.c` — 서보 구동
  - `HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1)`: 초기화 구역에서 PWM 시작
  - `servo_write_deg(deg)`: 0~180 클램프 후 `pulse_us = 1000 + deg/180*1000`
  - `__HAL_TIM_SET_COMPARE`에 µs 값을 그대로 넣음 → 타이머 1틱 = 1 µs, 주기 20 ms(50 Hz)로 설정되어 있다는 전제
- `05_설정과_코드.c` — DC 모터 구동 `motor_write(float u)`
  - `u`를 ±1로 클램프, 부호 → `GPIOB PIN_0` 방향 핀, 크기 → `fabsf(u) * 999` 듀티
  - `999` = ARR(주기 1000틱) 전제, TIM3 CH2 사용
  - `fabsf` 사용 → `<math.h>` 필요
  - 6·7강에서 그대로 재사용되는 액추에이터 인터페이스

## [선수 지식·연결]
- 4강: 메모리맵, GPIO 레지스터, 인터럽트·타이머 개념
- 6강 `06_통합_오늘의_결과물.c`: `motor_write`로 개루프 구동
- 7강 `03_ISR에서_조립.c`: PID 출력을 `motor_write(g_duty)`로 인가

## [실행 전 준비]
- STM32CubeIDE, Nucleo류 보드(LD2=PA5, 사용자 버튼=PC13 가정)
- CubeMX: TIM3 CH1(서보 50 Hz) / CH2(DC PWM), PB0 출력, PC13 EXTI
- 서보 모터, DC 모터 + 모터 드라이버, 외부 전원(모터 전원은 MCU 3.3 V에서 직접 공급 금지, GND 공통)

## [확인 포인트]
- 기대 결과: LED 깜빡임 → 버튼 반응 → 각도 지령대로 서보 회전 → `u` 부호·크기에 따른 모터 방향·속도 변화
- 흔한 실수
  - `HAL_TIM_PWM_Start` 누락 → 비교값을 바꿔도 출력 없음
  - 서보와 DC 모터 채널이 같은 TIM3를 쓰면 주파수(ARR·PSC)를 공유 → 50 Hz와 21 kHz 동시 불가, 실제 구성에서는 분리 필요
- 점검 질문
  - 오실로스코프로 본 서보 펄스 폭이 1.5 ms면 몇 도인가?
  - 인터럽트 방식에서 버튼 한 번에 토글이 여러 번 일어나면 원인은?
