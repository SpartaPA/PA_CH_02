#!/usr/bin/env bash
# [CH2 Physical AI] 41강. [실습] cuVSLAM·nvblox 3D 지도 생성·저장/로드
# 절: 서로 다른 세 가지 산출물
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

MAP_DIR=$(mktemp -d "$HOME/cuvslam_map_XXXXXX")
ros2 service call /visual_slam/save_map isaac_ros_visual_slam_interfaces/srv/FilePath "{file_path: '$MAP_DIR'}"

mkdir -p "$HOME/maps"
ros2 service call /nvblox_node/save_map nvblox_msgs/srv/FilePath "{file_path: '$HOME/maps/house.nvblx'}"
ros2 service call /nvblox_node/save_ply nvblox_msgs/srv/FilePath "{file_path: '$HOME/maps/house.ply'}"
