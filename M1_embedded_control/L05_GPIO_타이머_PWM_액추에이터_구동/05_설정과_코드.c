// [CH2 Physical AI] 5강. [실습] GPIO·타이머·PWM 액추에이터 구동 (DC/서보)
// 절: 4-2. 설정과 코드
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

void motor_write(float u)                        // u: -1.0 ~ +1.0
{
    if (u > 1.0f) u = 1.0f;
    if (u < -1.0f) u = -1.0f;
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0,
                      (u >= 0) ? GPIO_PIN_SET : GPIO_PIN_RESET);   // 방향
    uint32_t duty = (uint32_t)(fabsf(u) * 999);                     // 크기
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, duty);
}
