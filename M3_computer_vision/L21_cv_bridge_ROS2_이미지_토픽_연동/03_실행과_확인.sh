#!/usr/bin/env bash
# [CH2 Physical AI] 21강. [실습] cv_bridge ROS2 이미지 토픽 연동
# 절: 3. 실행과 확인
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# 터미널 1: 카메라  2: 검출 노드  3: 확인
ros2 topic echo /detection --once
ros2 run rqt_image_view rqt_image_view   # /image_annotated 선택
ros2 bag record /image_raw /camera_info /detection   # 22강에서 재생할 시험 데이터
