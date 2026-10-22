# [29강. [실습] YOLO 추론 ROS2 통합]
- 모듈: ④ 2D/3D 공간 인지 및 비전 AI
- 한 줄 요약: YOLO 추론을 ROS 2 노드로 감싸 표준 메시지 `vision_msgs/Detection2DArray`로 발행하고, 처리율·지연을 측정해 동작점을 고른 뒤, 박스를 바닥 평면과 교차시켜 3D 위치로 승격

## [핵심 개념]
- 표준 메시지 사용: `Detection2DArray` → 다른 노드·RViz·도구와 그대로 호환
  - `Detection2D.bbox`: 중심 `center.position.(x,y)` + 크기 `size_x`, `size_y`
  - `ObjectHypothesisWithPose.hypothesis`: `class_id`(문자열), `score`
- 최신 프레임 슬롯(드롭 정책)
  - 구독 콜백은 메시지 저장만, 무거운 추론은 타이머 루프에서 처리
  - 추론이 카메라보다 느리면 밀린 프레임은 버리고 가장 최신만 처리 → 지연 누적 방지
- `qos_profile_sensor_data`: best-effort·얕은 큐 → 센서 스트림에 적합
- 헤더(타임스탬프) 계승: 출력 `header = 입력 header` → 촬영 시각 기준 지연 측정·다른 센서와 시간 정합 가능
- 실시간성 지표
  - 처리율 [Hz]: `ros2 topic hz`
  - 지연: 현재 시각 − 메시지 스탬프(`ros2 topic delay`)
  - 입력 해상도·모델 크기 ↔ 처리율·정확도 사이의 동작점 선택
- 3D 승격(단안 + 평면 가정)
  - 박스 밑변 중심 $(u,\,v_c+h/2)$ = 물체가 바닥에 닿는 점이라고 가정
  - 광선 방향 $d_c=K^{-1}[u,v,1]^\top$ → World로 회전 $d_w=R_{wc}d_c$, 원점 $o=t_{wc}$
  - 평면 $z=z_0$과 교점: $s=\frac{z_0-o_z}{d_{w,z}}$, $P=o+s\,d_w$

## [파일별 내용]
- `01_yolo_node.ipynb` — 원본 `yolo_node.py` 핵심부, `YoloNode`(노드 이름 `yolo_detector`)
  - 파라미터: `model`(`yolov8n.pt`), `conf`(0.5), `iou`(0.45) → 25강의 두 임계값을 ROS 파라미터로
  - 구독 `/image_raw`(`sensor_msgs/Image`), 발행 `/detections`(큐 10)
  - `on_image`: `self.latest`에 저장만
  - `on_timer`(0.01 s 주기): 최신 메시지를 꺼내고 슬롯 비움 → `imgmsg_to_cv2(msg, "bgr8")` → YOLO → `xyxy`를 중심·크기로 변환해 발행
  - 빠진 맥락: `rclpy`·`Node`·`Image`·`qos_profile_sensor_data`·`YOLO`·`CvBridge` import, `self.bridge = CvBridge()` 생성, `main()`/`rclpy.spin`, 패키지 `setup.py`
- `02_실시간성_측정과_동작점_선택.sh` — 노드 실행 중 `/detections` 처리율·지연 측정 명령 2줄
- `03_3D_승격_어디에_까지.ipynb` — 검출 하나의 밑변 중심 `(u, v)` 계산 후 `ray_plane_intersect(u, v, K, T_world_cam, plane_z=0.0)`
  - `ray_plane_intersect`는 23강 `geometry.py`의 함수로 이 폴더에 정의 없음
  - `T_world_cam`: 카메라 → World 동차변환(카메라 설치 위치·자세)

## [선수 지식·연결]
- 21강: `cv_bridge`, 이미지 토픽 구독
- 23강: 역투영 광선, `geometry.py` 재사용
- 25강: Ultralytics 추론, `conf`·`iou` 의미
- 31강: 평면 가정 대신 실제 깊이로 3D 위치를 구하는 경로
- ⑨ 모듈 68강: 최신 프레임 슬롯·미스 정책의 확장

## [실행 전 준비]
- ROS 2 환경, `rclpy`, `cv_bridge`, `vision_msgs` 패키지
- `ultralytics`, 카메라 드라이버(예: `usb_cam`/`v4l2_camera`)가 `/image_raw` 발행
- 3D 승격: 카메라 $K$와 `T_world_cam`(설치 높이·기울기) 필요

## [확인 포인트]
- 기대 결과: `ros2 topic echo /detections`에 박스·클래스 이름·점수 출력, `hz`가 카메라 FPS 이하에서 안정
- 흔한 실수
  - 출력 헤더를 새 시각으로 채워 `delay`가 0에 가깝게 왜곡
  - QoS 불일치(카메라 reliable vs 구독 best-effort 등)로 메시지 미수신
  - `self.bridge` 미생성으로 `AttributeError`
  - 박스가 바닥에 닿지 않은 물체(테이블 위·공중)에 평면 가정 적용 → 큰 위치 오차
- 점검 질문
  - 콜백 안에서 바로 추론하면 큐에서 어떤 일이 생기는가?
  - 입력 해상도를 줄였을 때 처리율과 작은 물체 검출률은 어떻게 변하는가?
  - 카메라 기울기 오차 1°가 먼 물체의 바닥 교점에 미치는 영향은?
