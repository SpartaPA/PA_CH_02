#!/usr/bin/env bash
# [CH2 Physical AI] 42강. [실습] cuVSLAM 지도 재위치 추정·추적 복구
# 절: 1. 배선 — 시각 지도 로드와 TF 공급
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo map base_link
ros2 topic echo /visual_slam/status --once
ros2 topic echo /visual_slam/tracking/odometry --once
