// [CH2 Physical AI] 7강. [실습] PID 펌웨어 목표값 추종 (속도/위치)
// 절: 2. PID 모듈 구현
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

typedef struct {
    float Kp, Ki, Kd;
    float dt;                 // 제어 주기 [s]
    float out_min, out_max;   // 출력 포화 한계
    float integral;
    float meas_prev;          // 측정값 미분용 (derivative on measurement)
    float d_filt;             // 미분 필터 상태
    float d_alpha;            // 미분 EMA 계수 (0.1~0.3)
} PID;

float pid_step(PID *c, float ref, float meas)
{
    float e = ref - meas;

    // D: 측정값 미분 + EMA 필터 (3강 심화의 두 수정 모두 적용)
    float d_raw = -(meas - c->meas_prev) / c->dt;
    c->meas_prev = meas;
    c->d_filt += c->d_alpha * (d_raw - c->d_filt);

    // 잠정 출력
    float u = c->Kp * e + c->Ki * c->integral + c->Kd * c->d_filt;

    // anti-windup: 포화 방향으로 밀어붙이는 동안은 적분 동결 (조건부 적분)
    int saturating = (u > c->out_max && e > 0) || (u < c->out_min && e < 0);
    if (!saturating)
        c->integral += e * c->dt;

    // 최종 포화
    if (u > c->out_max) u = c->out_max;
    if (u < c->out_min) u = c->out_min;
    return u;
}

void pid_reset(PID *c) { c->integral = 0; c->d_filt = 0; c->meas_prev = 0; }
