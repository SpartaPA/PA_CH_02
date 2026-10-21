# [CH2 Physical AI] 43강. [실습] Nav2 다중 Waypoint 주행
# 절: 4. 이벤트 로거 — 45강의 데이터를 오늘부터
# 원본 경로: nav_logger.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# nav_logger.py — 구독: 액션 피드백·/plan(재계획 감지)·behavior_tree_log
#  기록(csv): 시각, 구간, 이벤트(START/REPLAN/RECOVERY/ARRIVE/FAIL), 위치, 소요
