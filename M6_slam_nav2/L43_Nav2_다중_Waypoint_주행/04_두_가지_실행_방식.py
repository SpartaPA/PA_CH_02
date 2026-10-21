# [CH2 Physical AI] 43강. [실습] Nav2 다중 Waypoint 주행
# 절: 3-2. 두 가지 실행 방식
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

nav.followWaypoints(poses)                     # ① 내장 Waypoint Follower
# vs
for p in poses:                                # ② goToPose 순차 호출 (우리의 선택)
    nav.goToPose(p); wait(); log_result(p)
