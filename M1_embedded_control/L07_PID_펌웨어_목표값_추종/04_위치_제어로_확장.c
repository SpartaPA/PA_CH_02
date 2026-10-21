// [CH2 Physical AI] 7강. [실습] PID 펌웨어 목표값 추종 (속도/위치)
// 절: 4. 위치 제어로 확장
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

float angle_deg = encoder_count() * 360.0f / CPR;          // 누적 각도
g_duty = pid_step(&g_pid_pos, g_target_deg, angle_deg);
