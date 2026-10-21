// [CH2 Physical AI] 6강. [실습] ADC·엔코더 센서 인터페이스
// 절: 5. 통합 — 오늘의 결과물
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

while (1)                                  // 메인 루프 (로깅 20Hz)
{
    float knob = adc_read_volt() / 3.3f;           // 0~1
    motor_write(knob);                              // 개루프: 듀티 직접 지정
    printf("%lu, %.2f, %.1f\r\n", HAL_GetTick(), knob, speed_rpm);
    HAL_Delay(50);
}
