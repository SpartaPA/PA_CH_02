# [CH2 Physical AI] 62강. [실습] 실패 케이스 분석·보정 전략 적용
# 절: 2. System ID — 실물이 시뮬을 가르친다
# 원본 경로: sysid.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# sysid.py — 57강 재생 오차를 목적 함수로 (58강 절차)
result = minimize(lambda xi: replay_error(xi, real_logs),
                  x0=nominal, method="CMA-ES")
# 추정 대상: 데드존 폭, 지연, 관절 0점 오프셋, 마찰 (민감도 확인된 것만)
