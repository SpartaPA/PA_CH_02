#!/usr/bin/env bash
# [CH2 Physical AI] 41강. [실습] cuVSLAM·nvblox 3D 지도 생성·저장/로드
# 절: 1. 배선 — 39강 회로도의 실물화
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# Isaac Sim 6.1: enable ROS 2 Bridge, open the configured camera scene, press Play.
# Activate the Isaac ROS 5.0 environment in each ROS terminal.
isaac-ros activate
source /opt/ros/lyrical/setup.bash

# Terminal 2: camera topics and calibration must match the official Sim example.
ros2 launch isaac_ros_cuvslam isaac_ros_visual_slam_isaac_sim.launch.py

# Terminal 3: live depth input, one camera, no duplicate Nav2 or static map-odom TF.
# Configure nvblox camera remaps and pose/TF source for cuVSLAM before launch.
ros2 launch nvblox_examples_bringup isaac_sim_example.launch.py num_cameras:=1 navigation:=False

# Terminal 4: visualization
rviz2 -d $(ros2 pkg prefix isaac_ros_cuvslam --share)/rviz/isaac_sim.cfg.rviz --ros-args -p use_sim_time:=true
