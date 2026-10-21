// [CH2 Physical AI] 7강. [실습] PID 펌웨어 목표값 추종 (속도/위치)
// 절: ISR에서 조립
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

PID g_pid = { .Kp=0, .Ki=0, .Kd=0, .dt=0.001f,
              .out_min=-1.0f, .out_max=1.0f, .d_alpha=0.2f };

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM7) {
        g_speed_rpm = measure_speed_rpm();          // 6강: 엔코더 증분+EMA
        g_duty = pid_step(&g_pid, g_target_rpm, g_speed_rpm);
        motor_write(g_duty);                        // 5강
    }
}
