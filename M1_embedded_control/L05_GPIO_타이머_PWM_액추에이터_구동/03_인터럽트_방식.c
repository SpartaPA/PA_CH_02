// [CH2 Physical AI] 5강. [실습] GPIO·타이머·PWM 액추에이터 구동 (DC/서보)
// 절: 2-2. 인터럽트 방식
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_13)
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);   // 짧게: 토글만 하고 리턴
}
/* USER CODE END 4 */
