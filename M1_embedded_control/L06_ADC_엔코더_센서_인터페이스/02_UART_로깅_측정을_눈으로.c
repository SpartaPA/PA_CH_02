// [CH2 Physical AI] 6강. [실습] ADC·엔코더 센서 인터페이스
// 절: 2. UART 로깅 — 측정을 눈으로
// ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

#include <stdio.h>
int _write(int file, char *ptr, int len)         // printf를 UART로 리다이렉트
{
    HAL_UART_Transmit(&huart2, (uint8_t*)ptr, len, HAL_MAX_DELAY);
    return len;
}
