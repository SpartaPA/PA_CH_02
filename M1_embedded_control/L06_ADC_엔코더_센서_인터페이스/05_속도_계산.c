// [CH2 Physical AI] 6강. [실습] ADC·엔코더 센서 인터페이스
// 절: 4-3. 속도 계산
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

#define CPR 1320.0f                       // 출력축 1회전당 카운트
volatile float speed_rpm = 0;

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)   // 10ms마다
{
    if (htim->Instance == TIM7) {
        static int32_t prev = 0;
        int32_t now = encoder_count();
        int32_t diff = now - prev;        // 오버플로도 자연 처리(부호 연산)
        prev = now;
        float rev_per_s = diff / CPR / 0.010f;
        speed_rpm = ema_speed(rev_per_s * 60.0f);   // 필터 적용
    }
}
