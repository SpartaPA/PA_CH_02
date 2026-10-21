#!/usr/bin/env bash
# [CH2 Physical AI] 43강. [실습] Nav2 다중 Waypoint 주행
# 절: 1. 풀스택 기동과 첫 주행
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 launch nav2_bringup navigation_launch.py params_file:=$HOME/nav2_params_cuvslam_nvblox.yaml use_sim_time:=true
