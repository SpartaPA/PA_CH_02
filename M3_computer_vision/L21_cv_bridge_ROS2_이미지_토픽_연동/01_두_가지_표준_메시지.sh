#!/usr/bin/env bash
# [CH2 Physical AI] 21강. [실습] cv_bridge ROS2 이미지 토픽 연동
# 절: 두 가지 표준 메시지
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

ros2 run usb_cam usb_cam_node_exe --ros-args -p video_device:=/dev/video0 \
    -p camera_info_url:=file:///home/user/.ros/camera_info/webcam.yaml
ros2 topic hz /image_raw          # 30Hz 근처?
ros2 run rqt_image_view rqt_image_view
