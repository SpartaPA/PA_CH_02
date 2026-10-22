# [43강. [실습] Nav2 다중 Waypoint 주행]
- 모듈: ⑥ SLAM 및 Nav2 자율주행
- 한 줄 요약: cuVSLAM·nvblox 기반 Nav2 풀스택을 띄우고, `nav2_simple_commander`로 파일에 정의된 여러 경유지를 순회하며 이벤트를 기록하는 순찰 노드 제작

## [핵심 개념]
- **Nav2 구조** → Behavior Tree(BT)가 전역 플래너(경로)·로컬 컨트롤러(속도 명령)·리커버리를 조율
  - 전역 플래너: costmap 위 최소 비용 경로(`/plan`)
  - 컨트롤러: 경로 추종 `cmd_vel` 생성
  - 리커버리: 막혔을 때 회전·후진·대기 등
- **costmap** → static/obstacle/inflation 레이어가 장애물을 비용장으로 변환, 이번 구성에서는 nvblox가 장애물 정보 공급
- **액션(action)** → 목표·피드백·결과를 갖는 장시간 작업 인터페이스
  - `NavigateToPose`(단일 목표), `FollowWaypoints`(목록)
  - 결과: `SUCCEEDED / CANCELED / FAILED`
- **Lifecycle 노드** → Nav2 노드가 active 상태가 되어야 명령 수락 → `waitUntilNav2Active()`
- **목표 자세 표현** → `PoseStamped`, 프레임은 반드시 `map`
  - 평면 yaw $\psi$ → 쿼터니언 $(0,0,\sin\frac{\psi}{2},\cos\frac{\psi}{2})$
- **설정과 코드 분리** → 경유지 좌표는 YAML 파일로, 코드는 순회 로직만
- **재계획(replan)** → 주행 중 `/plan`이 새로 발행되면 경로 재계산 발생 → 45강 지표의 원천

## [파일별 내용]
- `01_풀스택_기동과_첫_주행.sh` — `nav2_bringup navigation_launch.py`를 `params_file:=$HOME/nav2_params_cuvslam_nvblox.yaml`, `use_sim_time:=true`로 기동
  - 파라미터 파일 자체는 저장소에 없음(교안 별도 준비물)
  - `navigation_launch.py`는 지도 서버·AMCL 없이 내비게이션만 기동 → 위치는 cuVSLAM(42강)이 담당
- `02_patrol_node.ipynb` — `patrol_node.py` 핵심부(발췌)
  - `BasicNavigator()` 생성 → `waitUntilNav2Active()`
  - `goal.header.frame_id = "map"`, 위치 $(2.0,-1.5)$, `yaw_to_quat(1.57)` = 약 90° 방향 도착
  - `goToPose(goal)` → `isTaskComplete()` 루프 안에서 `getFeedback()`(남은 거리·경과 시간·리커버리 횟수) → `getResult()`
  - 빠진 맥락: `rclpy.init()`, `PoseStamped` import(`geometry_msgs.msg`), `yaw_to_quat` 정의, `TaskResult` 비교 로직, 종료 처리
- `03_waypoints.yaml` — `config/waypoints.yaml`
  - `kitchen / hallway / bedroom / dock` 4개, 각 `x, y, yaw`(m, rad)
  - 마지막 `dock`(원점) 복귀로 순찰 1회 완료
- `04_두_가지_실행_방식.ipynb` — 실행 방식 비교
  - ① `followWaypoints(poses)`: 내장 Waypoint Follower, 간단하지만 구간별 제어·기록이 제한적
  - ② `goToPose` 순차 호출(강의 선택): 구간마다 대기·결과 기록 가능 → 45강 측정에 유리
  - `wait()`, `log_result()`는 의사 함수
- `05_nav_logger.ipynb` — `nav_logger.py` 설계 주석만 존재
  - 구독: 액션 피드백, `/plan`(재계획 감지), `behavior_tree_log`
  - CSV 기록: 시각, 구간, 이벤트(`START/REPLAN/RECOVERY/ARRIVE/FAIL`), 위치, 소요

## [선수 지식·연결]
- 40강: Nav2 구조·lifecycle, 41·42강: 지도와 재위치 추정(`map` 프레임의 근거)
- 20강 계열: 쿼터니언, 모듈 ⑤: 설정 파일 분리 원칙
- 44강: 같은 순찰로 플래너·costmap 튜닝 비교, 45강: 로거 CSV로 성공률·소요시간·재계획 집계

## [실행 전 준비]
- 41·42강 환경 + 재위치 추정 완료 상태
- `nav2_bringup`, `nav2_simple_commander`(apt, ROS 2 Lyrical), PyYAML
- Nav2 파라미터 파일 `nav2_params_cuvslam_nvblox.yaml`

## [확인 포인트]
- 기대 결과: 4개 경유지를 순서대로 도착, 구간별 결과와 이벤트가 CSV에 남음
- 흔한 실수: `frame_id`를 `odom`/`base_link`로 지정, yaw를 쿼터니언 변환 없이 대입, lifecycle 대기 생략
- 점검 질문
  - `followWaypoints` 대신 `goToPose` 순차 호출을 택한 이유는?
  - `/plan` 메시지 수로 재계획을 세면 어떤 과대·과소 계수가 생길 수 있는가?
  - 경유지 하나가 `FAILED`일 때 다음 경유지로 넘어갈지 중단할지 어떻게 정할 것인가?
