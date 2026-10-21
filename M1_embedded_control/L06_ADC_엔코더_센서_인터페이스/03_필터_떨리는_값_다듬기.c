// [CH2 Physical AI] 6강. [실습] ADC·엔코더 센서 인터페이스
// 절: 3. 필터 — 떨리는 값 다듬기
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

float ema(float x)                                // alpha = 0.2
{
    static float y = 0;
    y = 0.2f * x + 0.8f * y;
    return y;
}
