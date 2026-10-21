# [CH2 Physical AI] 43강. [실습] Nav2 다중 Waypoint 주행
# 절: 2. 코드로 명령 — NavigateToPose 액션
# 원본 경로: patrol_node.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# patrol_node.py (핵심부) — nav2_simple_commander 사용
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

nav = BasicNavigator()
nav.waitUntilNav2Active()                      # lifecycle 대기 (40강)

goal = PoseStamped()
goal.header.frame_id = "map"                   # 반드시 map 프레임!
goal.pose.position.x, goal.pose.position.y = 2.0, -1.5
goal.pose.orientation = yaw_to_quat(1.57)      # 도착 방향 (Lv.1 20강 쿼터니언)

nav.goToPose(goal)
while not nav.isTaskComplete():
    fb = nav.getFeedback()                     # 남은 거리·경과 시간·리커버리 횟수
    ...
print(nav.getResult())                          # SUCCEEDED / CANCELED / FAILED
