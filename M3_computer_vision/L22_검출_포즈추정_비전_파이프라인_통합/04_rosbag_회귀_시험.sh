#!/usr/bin/env bash
# [CH2 Physical AI] 22강. [실습] 검출→포즈추정 비전 파이프라인 통합
# 절: 5-3. rosbag 회귀 시험
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 bag play session1/ --loop
ros2 topic hz /object_pose      # 처리율
ros2 topic delay /object_pose   # 프레임 촬영 → 포즈 발행까지의 지연
