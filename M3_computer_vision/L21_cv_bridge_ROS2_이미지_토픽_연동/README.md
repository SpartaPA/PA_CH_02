# [21강. [실습] cv_bridge ROS2 이미지 토픽 연동]
- 모듈: ③ 컴퓨터 비전 + 카메라 모델
- 한 줄 요약: 카메라 드라이버가 발행하는 `Image`·`CameraInfo` 토픽을 받아 `cv_bridge`로 OpenCV 배열로 바꾸고, 19강 색 검출기를 그대로 ROS 2 노드로 감싸 검출 결과·디버그 영상을 발행하는 실습

## [핵심 개념]
- **두 가지 표준 메시지**
  - `sensor_msgs/Image`: 픽셀 버퍼 + `height`/`width`/`encoding`/`step` + `header`(타임스탬프·`frame_id`)
  - `sensor_msgs/CameraInfo`: $K$(3×3), 왜곡계수 `d`, 해상도 등 → 20강 캘리브레이션 결과를 함께 전송
  - `usb_cam`은 `camera_info_url`의 YAML을 읽어 `/camera_info`로 발행
- **`cv_bridge`**
  - `imgmsg_to_cv2(msg, desired_encoding="bgr8")`: 메시지 → `(H, W, 3)` `uint8` ndarray
  - `cv2_to_imgmsg(arr, "bgr8")`: ndarray → 메시지
  - 인코딩을 명시해야 RGB/BGR 혼동이 없음
- **센서 QoS**
  - `qos_profile_sensor_data`: best-effort, 작은 큐 → 늦은 프레임보다 최신 프레임 우선
  - 발행 측과 QoS 호환이 안 되면 메시지가 오지 않음(8강 QoS 선택과 같은 맥락)
- **타임스탬프 계승**
  - 결과 메시지의 `header`에 원본 이미지 `header`를 복사 → "언제 찍힌 프레임의 결과인지" 보존
  - 후속 단계의 지연 측정(`ros2 topic delay`)과 센서 동기화의 전제
- **디버그 토픽 분리**: 결과 수치(`/detection`)와 시각화 영상(`/image_annotated`)을 따로 발행, 시각화 큐는 1
- **rosbag 기록**: 실제 카메라 입력을 저장해 두고 같은 입력으로 반복 시험(22강 회귀 시험)

## [파일별 내용]
- `01_두_가지_표준_메시지.sh` — 카메라 드라이버 실행과 확인
  - `usb_cam_node_exe`에 `video_device:=/dev/video0`, `camera_info_url:=file:///home/user/.ros/camera_info/webcam.yaml` 지정
  - `ros2 topic hz /image_raw`: 발행 주기 확인(주석: 30 Hz 근처인지)
  - `rqt_image_view`: 영상 육안 확인
  - 경로의 `/home/user`는 자기 계정 경로로 교체
- `02_color_detector_node` — 원본 `color_detector_node.py`(핵심부)
  - `ColorDetectorNode`: `/image_raw` 구독 → `ColorDetector.step` → `/detection`(`PointStamped`), `/image_annotated`(`Image`) 발행
  - `from color_detector import ColorDetector`: 19강 모듈을 수정 없이 재사용
  - `pt.point.x/y`에는 **픽셀 좌표**(`cx`, `cy`)가 들어감, 미터 단위 3D 점 아님(`z`는 0)
  - 빠진 맥락: `from rclpy.qos import qos_profile_sensor_data`, `load_cfg()`·`draw()` 구현, `main()`(`rclpy.init` → `spin` → `shutdown`), 패키지 `setup.py` 엔트리 포인트
- `03_실행과_확인.sh` — 터미널 3개 구성(1: 카메라, 2: 검출 노드, 3: 확인)
  - `ros2 topic echo /detection --once`: 결과 1건 확인
  - `rqt_image_view`에서 `/image_annotated` 선택
  - `ros2 bag record /image_raw /camera_info /detection`: 22강에서 재생할 시험 데이터 기록

## [선수 지식·연결]
- 19강: `ColorDetector`(`make_mask` + `detect` + EMA)
- 20강: `camera_params.npz`의 $K$·`dist` → `camera_info` YAML로 옮겨 드라이버에 제공
- 8강: ROS 2 노드·토픽·QoS 기본
- 22강: 이 노드 구조에 PnP·거리 추정을 붙이고, 여기서 기록한 bag으로 회귀 시험

## [실행 전 준비]
- ROS 2 환경(루트 README 기준 ROS 2 Lyrical), `usb_cam`, `cv_bridge`, `rqt_image_view` 패키지
- USB 웹캠(`/dev/video0`)과 장치 접근 권한
- 20강 결과를 담은 `camera_info` YAML
- 노드를 ROS 2 Python 패키지로 만들어 `colcon build` 후 `source install/setup.bash`

## [확인 포인트]
- 기대 결과: `/image_raw` 약 30 Hz, `/detection`에 공 중심 픽셀 좌표, `/image_annotated`에 표시된 영상
- 흔한 실수
  - QoS 불일치로 구독 콜백이 한 번도 호출되지 않음
  - `desired_encoding` 생략 후 드라이버가 `rgb8`을 보내 색이 뒤바뀜 → HSV 범위가 맞지 않음
  - `header`를 새로 만들어(현재 시각) 지연 측정이 무의미해짐
- 점검 질문
  - `/detection`의 `header.stamp`와 `/image_raw`의 `header.stamp`는 같아야 하는가?
  - 검출 노드 처리율이 카메라보다 느리면 best-effort QoS에서 어떤 일이 일어나는가?
  - `PointStamped`에 픽셀 좌표를 담는 것의 한계는 무엇이고 22강은 이를 어떻게 바꾸는가?
