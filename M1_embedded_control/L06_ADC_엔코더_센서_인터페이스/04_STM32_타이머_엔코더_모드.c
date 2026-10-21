// [CH2 Physical AI] 6강. [실습] ADC·엔코더 센서 인터페이스
// 절: 4-2. STM32 타이머 엔코더 모드
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

HAL_TIM_Encoder_Start(&htim2, TIM_CHANNEL_ALL);

int32_t encoder_count(void)
{
    return (int32_t)__HAL_TIM_GET_COUNTER(&htim2);   // 회전 방향 따라 증감
}
