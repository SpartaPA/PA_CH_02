// [CH2 Physical AI] 5강. [실습] GPIO·타이머·PWM 액추에이터 구동 (DC/서보)
// 절: 1-2. 빌드–플래시–관찰 사이클
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

/* USER CODE BEGIN WHILE */
while (1)
{
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);   // LD2 반전
    HAL_Delay(500);                          // 500ms 대기
/* USER CODE END WHILE */
}
