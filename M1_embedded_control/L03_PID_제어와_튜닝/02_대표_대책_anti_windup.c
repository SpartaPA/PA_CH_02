// [CH2 Physical AI] 3강. PID 제어와 튜닝 (P·I·D·Ziegler–Nichols·anti-windup)
// 절: 대표 대책 (anti-windup)
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

float u = c->Kp*e + c->Ki*c->integral + c->Kd*deriv;
if (u > U_MAX)      { u = U_MAX; if (e > 0) c->integral -= e*dt; }  // 쌓은 것 취소
else if (u < U_MIN) { u = U_MIN; if (e < 0) c->integral -= e*dt; }
