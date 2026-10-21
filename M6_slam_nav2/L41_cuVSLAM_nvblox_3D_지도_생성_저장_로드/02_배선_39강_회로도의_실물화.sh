#!/usr/bin/env bash
# [CH2 Physical AI] 41강. [실습] cuVSLAM·nvblox 3D 지도 생성·저장/로드
# 절: 1. 배선 — 39강 회로도의 실물화
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 topic list -t
ros2 topic echo /clock --once
ros2 topic echo /visual_slam/tracking/odometry --once
ros2 topic echo /visual_slam/status --once
ros2 run tf2_tools view_frames
