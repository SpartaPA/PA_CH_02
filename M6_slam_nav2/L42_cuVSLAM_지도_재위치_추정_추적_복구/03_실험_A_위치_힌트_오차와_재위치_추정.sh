#!/usr/bin/env bash
# [CH2 Physical AI] 42강. [실습] cuVSLAM 지도 재위치 추정·추적 복구
# 절: 실험 A — 위치 힌트 오차와 재위치 추정
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 service call /visual_slam/localize_in_map isaac_ros_visual_slam_interfaces/srv/LocalizeInMap "{map_folder_path: '$MAP_DIR', pose_hint: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}"
