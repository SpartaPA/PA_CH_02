#!/usr/bin/env bash
# [CH2 Physical AI] 8강. [실습] micro-ROS ROS2 네트워크 연동
# 절: 3-2. 조작과 관찰
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# 목표 속도 100 RPM 지령
ros2 topic pub --once /motor/target std_msgs/msg/Float32 "{data: 100.0}"

# 실시간 그래프
rqt_plot /motor/state/data[0]     # speed_rpm 곡선
