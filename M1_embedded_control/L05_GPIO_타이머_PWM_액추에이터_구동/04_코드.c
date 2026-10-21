// [CH2 Physical AI] 5강. [실습] GPIO·타이머·PWM 액추에이터 구동 (DC/서보)
// 절: 3-2. 코드
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

/* USER CODE BEGIN 2 */
HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
/* USER CODE END 2 */

/* USER CODE BEGIN 4 */
void servo_write_deg(float deg)                  // 0~180도 → 1000~2000us
{
    if (deg < 0) deg = 0;
    if (deg > 180) deg = 180;
    uint32_t pulse_us = 1000 + (uint32_t)(deg / 180.0f * 1000.0f);
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, pulse_us);
}
/* USER CODE END 4 */
