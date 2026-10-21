// [CH2 Physical AI] 4강. MCU와 주변장치 (Cortex-M·GPIO·인터럽트·타이머·PWM)
// 절: 메모리맵 — "모든 것은 주소다"
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

// bare-metal: GPIOA의 출력 데이터 레지스터(ODR) 5번 비트를 1로
GPIOA->ODR |= (1 << 5);            // 레지스터 직접 조작

// HAL(추상화 라이브러리): 같은 일을 함수로
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
