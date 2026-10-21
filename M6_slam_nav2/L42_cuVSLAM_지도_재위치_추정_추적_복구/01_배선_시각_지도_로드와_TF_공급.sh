#!/usr/bin/env bash
# [CH2 Physical AI] 42강. [실습] cuVSLAM 지도 재위치 추정·추적 복구
# 절: 1. 배선 — 시각 지도 로드와 TF 공급
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

isaac-ros activate
source /opt/ros/lyrical/setup.bash
ros2 launch isaac_ros_cuvslam isaac_ros_visual_slam_isaac_sim.launch.py
# Start the same Isaac Sim camera scene and press Play.
# Use the saved map and pose hint in experiment A below.
# Restore nvblox state separately; do not start AMCL.
