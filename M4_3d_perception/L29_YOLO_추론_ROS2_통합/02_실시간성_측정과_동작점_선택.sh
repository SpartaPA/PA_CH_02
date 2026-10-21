#!/usr/bin/env bash
# [CH2 Physical AI] 29강. [실습] YOLO 추론 ROS2 통합
# 절: 2. 실시간성 측정과 동작점 선택
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 topic hz /detections          # 실제 처리율
ros2 topic delay /detections       # 촬영→발행 지연 (스탬프 계승 덕에 측정 가능)
