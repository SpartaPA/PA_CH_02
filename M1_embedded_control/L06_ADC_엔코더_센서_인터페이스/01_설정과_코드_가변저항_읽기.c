// [CH2 Physical AI] 6강. [실습] ADC·엔코더 센서 인터페이스
// 절: 1-2. 설정과 코드 (가변저항 읽기)
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

uint16_t adc_read_raw(void)
{
    HAL_ADC_Start(&hadc1);
    HAL_ADC_PollForConversion(&hadc1, 10);      // 변환 완료 대기 (max 10ms)
    return HAL_ADC_GetValue(&hadc1);            // 0~4095
}

float adc_read_volt(void)
{
    return adc_read_raw() * 3.3f / 4095.0f;
}
