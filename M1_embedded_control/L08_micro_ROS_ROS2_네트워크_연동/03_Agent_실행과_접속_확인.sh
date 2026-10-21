#!/usr/bin/env bash
# [CH2 Physical AI] 8강. [실습] micro-ROS ROS2 네트워크 연동
# 절: 3-1. Agent 실행과 접속 확인
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 node list          #  /motor_controller  ← MCU가 노드로 보인다!
ros2 topic list         #  /motor/state, /motor/target
ros2 topic hz /motor/state    # ≈ 50Hz — 우리가 설계한 주기
