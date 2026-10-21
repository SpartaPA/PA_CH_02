#!/usr/bin/env bash
# [CH2 Physical AI] 41강. [실습] cuVSLAM·nvblox 3D 지도 생성·저장/로드
# 절: 재로드 확인
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 service call /nvblox_node/load_map nvblox_msgs/srv/FilePath "{file_path: '$HOME/maps/house.nvblx'}"
ros2 service list -t
ros2 topic list -t
