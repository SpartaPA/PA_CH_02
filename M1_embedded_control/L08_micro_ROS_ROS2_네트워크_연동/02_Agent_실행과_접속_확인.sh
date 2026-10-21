#!/usr/bin/env bash
# [CH2 Physical AI] 8강. [실습] micro-ROS ROS2 네트워크 연동
# 절: 3-1. Agent 실행과 접속 확인
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# PC (Ubuntu): Agent 설치 후 실행 — 시리얼 장치와 속도 지정
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 -b 115200
