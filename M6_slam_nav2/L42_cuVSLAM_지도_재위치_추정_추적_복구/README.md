# [42강. [실습] cuVSLAM 지도 재위치 추정·추적 복구]
- 모듈: ⑥ SLAM 및 Nav2 자율주행
- 한 줄 요약: 41강에서 저장한 cuVSLAM 지도를 불러와 `localize_in_map`으로 지도 좌표계 안의 현재 위치를 다시 찾고, TF 공급과 추적 상태를 점검하는 실습

## [핵심 개념]
- **재위치 추정(relocalization)** → 지도는 있으나 현재 위치를 모르는 상태에서 관측을 지도 특징과 대조해 자세 복원
  - "납치된 로봇(kidnapped robot)" 문제의 해결 수단
- **위치 힌트(pose hint)** → 탐색 초기값
  - 정답 근처일수록 수렴이 빠르고 안정적, 오차가 크면 실패하거나 엉뚱한 곳에 매칭될 수 있음 → 실험 A의 주제
- **추적(tracking) vs 재위치 추정**
  - 추적: 직전 프레임에서 이어지는 연속 추정(VO)
  - 추적 손실(빠른 회전·질감 부족·가림) 후 지도와 재대조해 복구
- **TF 공급** → 재위치 추정이 성공해야 `map → base_link` 변환이 지도 기준으로 정렬
  - `map→odom`은 지도 정합 결과, `odom→base_link`는 연속 오도메트리
- **AMCL을 쓰지 않는 이유** → cuVSLAM이 이미 `map` 기준 자세를 공급, AMCL까지 띄우면 같은 변환을 두 곳이 발행해 충돌(주석: "do not start AMCL")
- **지도 상태 분리** → 시각 지도(cuVSLAM)와 3D 지도(nvblox)는 별도 복원 대상

## [파일별 내용]
- `01_배선_시각_지도_로드와_TF_공급.sh` — 환경 활성화 후 cuVSLAM Isaac Sim launch 기동
  - 같은 Isaac Sim 카메라 장면을 열고 Play(수동)
  - 저장 지도·위치 힌트는 실험 A(`03`)에서 사용
  - nvblox 상태는 별도 복원(41강 `load_map`), AMCL은 기동 금지
- `02_배선_시각_지도_로드와_TF_공급.sh` — 점검 명령
  - `view_frames`: TF 트리 구조
  - `tf2_echo map base_link`: 지도 기준 로봇 자세를 실시간 출력 → 재위치 추정 전후 값 비교
  - `/visual_slam/status`, `/visual_slam/tracking/odometry` 1회 수신
- `03_실험_A_위치_힌트_오차와_재위치_추정.sh` — `/visual_slam/localize_in_map` 서비스 호출(`LocalizeInMap`)
  - `map_folder_path`: 41강에서 저장한 `$MAP_DIR`
  - `pose_hint`: 위치 $(0,0,0)$, 쿼터니언 $(0,0,0,1)$ = 원점·회전 없음
  - 실험 방법: 힌트를 실제 위치에서 일부러 어긋나게 바꿔 가며 성공 여부·결과 자세 비교
  - 주의: `$MAP_DIR`은 41강 셸에서 정한 변수 → 새 터미널이면 직접 경로를 지정해야 함

## [선수 지식·연결]
- 41강: cuVSLAM 지도 폴더(`save_map`)와 `.nvblx` 저장·로드
- 37~39강: 베이즈 필터의 예측·갱신, 루프 폐합
- 20강 계열: 쿼터니언 표기 $(x,y,z,w)$, 단위 회전은 $w=1$
- 43~45강: 재위치 추정된 `map` 프레임 위에서 Nav2 목표 지정, 45강 벤치마크 러너의 "지도 로드 → 위치 힌트 → 위치 확인" 단계로 재사용

## [실행 전 준비]
- 41강과 동일 환경(Isaac Sim 6.1, Isaac ROS 5.0, ROS 2 Lyrical, NVIDIA GPU)
- 41강에서 저장한 cuVSLAM 지도 폴더 경로
- `tf2_ros`, `tf2_tools`

## [확인 포인트]
- 기대 결과: 서비스 응답 성공 후 `tf2_echo map base_link`가 지도 기준 자세를 안정적으로 출력
- 흔한 실수: 빈 `$MAP_DIR`로 호출, AMCL 동시 기동으로 TF 충돌, 장면 Play 전 호출
- 점검 질문
  - 위치 힌트 오차를 키울 때 어느 지점에서 실패가 시작되는가?
  - 추적 손실과 재위치 추정 실패는 `/visual_slam/status`에서 어떻게 구분되는가?
  - 재위치 추정 직후 `map→odom` 변환이 갑자기 바뀌는 것은 정상인가?
