// [CH2 Physical AI] 3강. PID 제어와 튜닝 (P·I·D·Ziegler–Nichols·anti-windup)
// 절: 2. 이산화 — MCU 위의 PID
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

// 제어 주기 dt마다 호출 (7강에서 타이머 인터럽트로 구동)
float pid_step(PID *c, float ref, float meas, float dt)
{
    float e = ref - meas;                 // 오차
    c->integral += e * dt;                // I: 누적 (사각형 근사)
    float deriv = (e - c->e_prev) / dt;   // D: 차분 근사
    c->e_prev = e;
    return c->Kp * e + c->Ki * c->integral + c->Kd * deriv;
}
