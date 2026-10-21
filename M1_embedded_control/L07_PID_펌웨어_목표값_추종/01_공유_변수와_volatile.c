// [CH2 Physical AI] 7강. [실습] PID 펌웨어 목표값 추종 (속도/위치)
// 절: 1-2. 공유 변수와 volatile
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

volatile float g_target_rpm = 0;     // 메인 루프가 쓰고 ISR이 읽음
volatile float g_speed_rpm  = 0;     // ISR이 쓰고 메인 루프가 읽음
volatile float g_duty       = 0;     // ISR이 쓰고 메인 루프가 읽음(로깅용)
