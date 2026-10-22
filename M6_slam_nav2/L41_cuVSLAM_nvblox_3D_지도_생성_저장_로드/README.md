# [41강. [실습] cuVSLAM·nvblox 3D 지도 생성·저장/로드]
- 모듈: ⑥ SLAM 및 Nav2 자율주행
- 한 줄 요약: Isaac Sim 카메라 장면에 cuVSLAM(위치 추정)과 nvblox(3D 재구성)를 붙여 지도를 만들고, 성격이 다른 세 가지 산출물로 저장·재로드하는 실습

## [핵심 개념]
- **SLAM** → 위치($x_t$)와 지도($m$)를 동시에 추정: $p(x_{1:t},m\mid z_{1:t},u_{1:t})$
  - 지도 없이 위치를 모르고, 위치 없이 지도를 못 만드는 순환 문제를 함께 풂
- **cuVSLAM(시각-관성 SLAM)** → 카메라 특징점 추적으로 자세 추정, 결과는 `/visual_slam/tracking/odometry`와 TF로 공급
  - 루프 폐합: 다시 찾은 장소의 제약을 포즈 그래프에 넣어 누적 드리프트 분산
- **nvblox(3D 재구성)** → 깊이 영상 + 카메라 자세로 복셀 지도(TSDF/ESDF 계열) 갱신, 이를 2D costmap으로 내보내 Nav2에 공급
  - nvblox는 "자세를 받아 지도를 쌓는" 쪽 → 자세 공급원(cuVSLAM)과 TF 설정이 맞아야 지도가 어긋나지 않음
- **TF 사슬** → `map → odom → base_link → 카메라`
  - 같은 변환을 두 노드가 동시에 발행하면(예: 정적 `map→odom` + SLAM) TF 충돌 → 스크립트 주석의 "no duplicate ... static map-odom TF"
- **시뮬레이션 시간** → Isaac Sim이 `/clock` 발행, 모든 노드가 `use_sim_time:=true`로 같은 시계 사용
- **세 가지 산출물**(서로 용도가 다름)
  - cuVSLAM 지도 폴더: 재위치 추정용 시각 특징 지도(42강 `localize_in_map` 입력)
  - `.nvblx`: nvblox 내부 상태 → 재로드해 3D 지도·costmap 복원
  - `.ply`: 점/메시 파일 → 외부 뷰어 확인용, 재로드 대상 아님

## [파일별 내용]
- `01_배선_39강_회로도의_실물화.sh` — 39강에서 설계한 구성을 실제 터미널 4개로 기동
  - Isaac Sim 6.1에서 ROS 2 Bridge 활성화 → 장면 열고 Play(수동 단계, 주석)
  - `isaac-ros activate` + `source /opt/ros/lyrical/setup.bash`: 각 터미널마다 환경 활성화
  - 터미널 2: `isaac_ros_visual_slam_isaac_sim.launch.py` — 카메라 토픽·캘리브레이션이 공식 Sim 예제와 일치해야 함
  - 터미널 3: `nvblox_examples_bringup isaac_sim_example.launch.py num_cameras:=1 navigation:=False` — 카메라 1대, Nav2 중복 기동 방지
  - 터미널 4: `rviz2`에 cuVSLAM 제공 설정 파일 로드, `use_sim_time:=true`
- `02_배선_39강_회로도의_실물화.sh` — 배선 점검 명령 모음
  - `ros2 topic list -t`(토픽·타입), `/clock` 1회 수신(시뮬 시간 흐름), 오도메트리·`/visual_slam/status` 1회 수신
  - `tf2_tools view_frames`: TF 트리를 PDF로 출력해 끊김·중복 확인
- `03_서로_다른_세_가지_산출물.sh` — 지도 저장 서비스 호출
  - `MAP_DIR=$(mktemp -d ...)`: cuVSLAM 지도용 새 폴더, `/visual_slam/save_map`(`FilePath` 서비스)
  - `/nvblox_node/save_map` → `~/maps/house.nvblx`, `/nvblox_node/save_ply` → `~/maps/house.ply`
  - 주의: `MAP_DIR`은 셸 변수 → 42강에서 쓰려면 경로를 따로 기록해 둬야 함
- `04_재로드_확인.sh` — `/nvblox_node/load_map`으로 `.nvblx` 복원 후 서비스·토픽 목록 재확인

## [선수 지식·연결]
- 37~39강: 베이즈 필터·루프 폐합 이론, 39강 구성도(이 강의의 "배선" 원본)
- 21강: RViz2·토픽 기반 확인 습관
- 42강: 여기서 저장한 `MAP_DIR`로 재위치 추정
- 43강 이후: nvblox costmap 위에서 Nav2 주행(`navigation:=False`로 이번엔 Nav2 제외)

## [실행 전 준비]
- Isaac Sim 6.1(ROS 2 Bridge), Isaac ROS 5.0 환경(`isaac-ros activate`), ROS 2 Lyrical
- 패키지: `isaac_ros_cuvslam`, `nvblox_examples_bringup`, `tf2_tools`, `rviz2`
- NVIDIA GPU 필요(cuVSLAM·nvblox 모두 CUDA 기반)

## [확인 포인트]
- 기대 결과: RViz에서 카메라 이동에 따라 자세 궤적과 3D 복셀 지도가 함께 자람, `~/maps/`에 `.nvblx`·`.ply` 생성
- 흔한 실수: Play를 누르지 않아 `/clock` 무수신, `use_sim_time` 누락, `map→odom` TF 중복 발행
- 점검 질문
  - `.nvblx`와 `.ply`는 각각 무엇을 위해 저장하는가?
  - cuVSLAM 지도 폴더 없이 nvblox 지도만 있으면 다음 실행에서 로봇은 자기 위치를 알 수 있는가?
  - `view_frames` 결과에서 `map→odom`을 누가 발행하는지 설명할 수 있는가?
