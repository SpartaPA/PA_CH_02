# [22강. [실습] 검출→포즈추정 비전 파이프라인 통합]
- 모듈: ③ 컴퓨터 비전 + 카메라 모델
- 한 줄 요약: 경로 A(ArUco → PnP → `PoseStamped`)와 경로 B(색 검출 → 아는 크기로 거리 추정)로 2D 검출을 3D 위치로 올리고, RViz2로 시각화하며 rosbag으로 처리율·지연을 회귀 시험하는 모듈 ③ 종합 실습

## [핵심 개념]
- **경로 A: ArUco + PnP**
  - ArUco 마커: ID를 가진 정사각형 패턴 → 네 꼭짓점이 곧 순서가 정해진 2D-3D 대응점
  - 마커 중심을 원점으로 한 꼭짓점 3D 좌표 $(\pm\frac{s}{2},\pm\frac{s}{2},0)$, $s$ = 마커 한 변 실측
  - `solvePnP` → `rvec`/`tvec` → 쿼터니언 변환 후 `PoseStamped` 발행
  - 3D 점 순서는 ArUco 코너 반환 순서(좌상 → 우상 → 우하 → 좌하)와 일치해야 함
- **재투영 오차 게이트**
  - 구한 포즈로 꼭짓점을 다시 투영해 검출 코너와의 픽셀 오차 계산
  - 임계(코드: 2.0 px) 초과 포즈는 발행하지 않음 → 나쁜 값을 내보내지 않는 것이 하류 안전
- **경로 B: 단안 거리 추정**
  - 깊이: $Z=\frac{f_x\cdot D}{d_{px}}$, 코드에서 $d_{px}=2r_{px}$(원 반지름의 두 배)
  - 역투영: $X=\frac{(u-c_x)Z}{f_x},\;Y=\frac{(v-c_y)Z}{f_y}$ (17강 투영 사슬의 역방향)
  - 크기 $D$를 아는 물체에서만 성립(18강 단안 모호성)
- **좌표계**
  - OpenCV 카메라 좌표: $x$ 오른쪽, $y$ 아래, $z$ 전방(광학 프레임)
  - ROS 바디 좌표 규약은 $x$ 전방 → RViz2 Fixed Frame과 `frame_id`의 축 규약 차이 주의
- **회귀 시험**
  - 같은 bag을 반복 재생해 처리율(`hz`)과 촬영 → 발행 지연(`delay`)을 측정, 코드 변경 전후 비교
  - `delay`는 메시지 `header.stamp` 기준 → 원본 타임스탬프 계승(21강)이 전제

## [파일별 내용]
- `01_aruco_pose_node` — 원본 `aruco_pose_node.py`(핵심부), 경로 A
  - `ArucoDetector` + `DICT_4X4_50` 사전, `MARKER = 0.05`(마커 한 변 실측 [m])
  - `OBJ`: 4×3 `float32` 꼭짓점 좌표, `MARKER / 2`배
  - `on_image`: `self.K`가 없으면(`/camera_info` 미수신) 건너뜀 → 마커 검출 → `solvePnP(OBJ, corners[0], ...)` → 재투영 오차 2.0 px 초과 시 경고 후 폐기 → `PoseStamped` 발행
  - `corners[0]`: 첫 번째로 검출된 마커만 사용(ID 확인 없음)
  - 빠진 맥락: `/camera_info` 구독 콜백(`self.K`, `self.dist` 채움), `reproj_error`(`projectPoints` 기반), `to_pose_stamped`(`Rodrigues` → 쿼터니언, `header` 계승), 구독·발행자 생성
- `02_경로_B_색_검출_거리_추정` — 3줄 발췌
  - `BALL_DIAMETER`: 공 실제 지름[m], `r_px`: 검출 원의 픽셀 반지름
  - `self.fx`, `self.cx`, `self.cy`, `self.fy`: `CameraInfo`의 $K$ 원소
  - 주의: 여기의 `self.cx`는 주점 $c_x$이며 19강 EMA의 `self.cx`(검출 중심)와 다른 의미, 검출 중심은 지역 변수 `cx`, `cy`
  - 빠진 맥락: `r_px`를 구하는 방법(예: `cv2.minEnclosingCircle`), 결과 메시지 발행
- `03_RViz2_시각화_3D로_보는_첫_순간.sh` — `rviz2` 실행
  - 주석: Fixed Frame `camera_link`, Marker·Image 디스플레이 추가
- `04_rosbag_회귀_시험.sh`
  - `ros2 bag play session1/ --loop`: 기록한 bag 반복 재생(21강 기록 데이터, 폴더명은 기록 시 지정한 이름)
  - `ros2 topic hz /object_pose`: 처리율
  - `ros2 topic delay /object_pose`: 프레임 촬영 → 포즈 발행 지연

## [선수 지식·연결]
- 17강: 투영식과 역투영, 18강: PnP·재투영 오차·단안 모호성
- 19강: 색 검출기, 20강: $K$·`dist`, 21강: `cv_bridge` 노드 구조·`CameraInfo`·bag 기록
- 23강(M4): 좌표 사슬 `project`/`backproject`와 OpenCV↔ROS 좌표 규약
- 24·28강(M4): PnP 심화·RANSAC, 29강: YOLO 박스를 3D로 승격

## [실행 전 준비]
- ROS 2 환경, `cv_bridge`, `rviz2`, OpenCV(`cv2.aruco.ArucoDetector`를 쓰므로 OpenCV 4.7 이상의 aruco 포함 빌드)
- `DICT_4X4_50` 마커 인쇄물(한 변을 실측해 `MARKER`에 반영), 지름을 아는 단색 공
- 캘리브레이션된 카메라(`/camera_info` 발행) 또는 21강에서 기록한 bag

## [확인 포인트]
- 기대 결과: 마커를 움직이면 RViz2의 포즈가 따라 움직이고, 자로 잰 거리와 `tvec`의 $z$가 대략 일치
- 흔한 실수
  - `MARKER`·`BALL_DIAMETER`를 실측하지 않아 거리가 비례적으로 틀림
  - `OBJ` 꼭짓점 순서가 코너 순서와 달라 포즈가 뒤집힘
  - `/camera_info`가 오지 않아 `on_image`가 계속 조기 반환
  - Fixed Frame과 메시지 `frame_id` 불일치로 RViz2에 아무것도 안 보임
- 점검 질문
  - 마커가 비스듬할 때 경로 A와 경로 B 중 어느 쪽 거리 추정이 더 믿을 만한가?
  - 공이 화면 가장자리에 있을 때 경로 B에 왜곡 보정이 필요한 이유는?
  - `topic delay`가 커졌다면 처리율 저하와 어떻게 구분하는가?
