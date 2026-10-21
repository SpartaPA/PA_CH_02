# [CH2 Physical AI] 60강. [실습] 도메인 랜덤화 학습 환경 구축
# 절: 4. 커리큘럼 — ADR의 구현
# 원본 경로: adr.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# adr.py — 성공률 연동 폭 확대 (56강 계단의 구현)
if recent_success_rate > 0.8:
    widen_all(cfg, step=0.05)        # 각 축의 폭을 5%p 확대
elif recent_success_rate < 0.5:
    narrow_all(cfg, step=0.05)       # 후퇴도 가능
