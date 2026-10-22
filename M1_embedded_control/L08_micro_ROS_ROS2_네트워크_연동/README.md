# [8강. [실습] micro-ROS ROS2 네트워크 연동]
- 모듈: ① 임베디드 제어 기초
- 한 줄 요약: 7강 모터 제어 펌웨어를 micro-ROS 노드로 만들어 시리얼로 PC의 Agent에 붙이고, ROS 2 토픽으로 목표 속도를 보내고 상태를 그래프로 관찰

## [핵심 개념]
- micro-ROS 구조
  - MCU: rclc API로 노드·퍼블리셔·서브스크라이버 생성(XRCE-DDS 클라이언트)
  - PC: `micro_ros_agent`가 시리얼(또는 UDP) 너머의 MCU를 ROS 2 DDS 그래프에 대리 참여시킴
- rclc 초기화 순서: allocator/support → node → publisher·subscription·timer → executor
- executor
  - 등록한 타이머·구독 콜백을 `rclc_executor_spin_some()` 호출 시점에 실행
  - 핸들 수(코드는 2: 타이머 1 + 구독 1)를 미리 지정
- 실시간 분리
  - 1 kHz PID는 하드웨어 타이머 ISR(7강)
  - 50 Hz 통신은 executor(메인 루프) → 통신 지연이 제어 주기를 흔들지 않음
- 토픽 설계
  - `/motor/state`: `std_msgs/Float32MultiArray` [speed_rpm, duty], 50 Hz(20 ms 타이머)
  - `/motor/target`: `std_msgs/Float32` 목표 RPM
- QoS: 작은 시리얼 링크에서는 best-effort/reliable 선택을 신중히(코드는 `_default` = reliable)

## [파일별 내용]
- `01_노드_코드.c` — MCU 쪽 micro-ROS 노드
  - `state_timer_cb()`: `g_speed_rpm`, `g_duty`를 배열 메시지에 담아 publish
  - `target_cb()`: 수신값을 `g_target_rpm`에 저장 → 다음 ISR 주기에 PID 반영
  - `microros_task()`: 노드 이름 `motor_controller`, 초기화 후 `while(1)` spin(10 ms 타임아웃)
  - 발췌: 전역 `support`, `node`, `allocator`, `executor`, 메시지 변수 선언과 시리얼 transport 설정 생략
  - 주의: `state_msg.data.data`는 사전에 버퍼 할당(`data.capacity`, `data.size = 2`)이 필요 — 코드에 보이지 않음
  - `rcl_publish` 등 반환값 검사 생략
- `02_Agent_실행과_접속_확인.sh` — PC에서 Agent 실행: `serial --dev /dev/ttyACM0 -b 115200`
- `03_Agent_실행과_접속_확인.sh` — 접속 확인: `ros2 node list`, `ros2 topic list`, `ros2 topic hz /motor/state`(≈50 Hz)
- `04_조작과_관찰.sh` — `ros2 topic pub --once`로 100 RPM 지령, `rqt_plot /motor/state/data[0]`으로 속도 곡선 확인

## [선수 지식·연결]
- 7강: `volatile` 공유 변수와 ISR 기반 PID(이 노드는 그 변수만 읽고 씀)
- ROS 2 기초: 노드·토픽·메시지 타입·QoS
- 상위 PC 노드(예: 비전·계획 노드)가 토픽으로 MCU 제어기를 지휘하는 구조의 기본형

## [실행 전 준비]
- MCU: micro-ROS 정적 라이브러리를 포함한 펌웨어 프로젝트, 시리얼 transport 설정
- PC: ROS 2 + `micro_ros_agent` 패키지, `rqt_plot`
- 시리얼 장치 권한(`dialout` 그룹), 장치명(`/dev/ttyACM0`)과 보레이트 일치

## [확인 포인트]
- 기대 결과: `ros2 node list`에 `/motor_controller`, 100 RPM 지령 후 그래프가 목표로 수렴
- 흔한 실수
  - Agent를 MCU보다 늦게 띄우면 세션 미생성 → MCU 리셋 필요
  - 시리얼 모니터 등 다른 프로그램이 같은 포트 점유
- 점검 질문
  - `topic hz`가 50 Hz보다 낮게 나오면 어떤 원인(보레이트, 메시지 크기, spin 주기)을 의심하는가?
  - 목표 속도 토픽을 best-effort로 바꾸면 어떤 장단점이 있는가?
