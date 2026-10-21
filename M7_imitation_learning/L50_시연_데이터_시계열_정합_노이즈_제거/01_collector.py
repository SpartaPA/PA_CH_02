# [CH2 Physical AI] 50강. [실습] 시연 데이터 시계열 정합·노이즈 제거
# 절: 1. 수집기 — 마우스가 전문가다
# 원본 경로: collector.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# collector.py 사용법
# python collector.py --episodes 60 --seed 7
#  에피소드마다 물체 위치가 5x5 격자+지터로 배치 (46강 다양성 프로토콜)
#  r 키 = 이번 에피소드 폐기, 스페이스 = 성공 마킹
