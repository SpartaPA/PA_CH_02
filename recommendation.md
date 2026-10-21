# [Recommendation — 진짜 추천하는 3권]
- `reference.md`의 8권 중, 이 저장소의 코드를 이해하는 데 가장 효과가 큰 3권만 골랐습니다
- 고른 기준: 교안 코드와 직접 맞닿는 범위가 넓은가, 한 권으로 한 모듈 전체를 받쳐 주는가
- 나머지 5권은 해당 주제를 더 깊이 볼 때 펼치는 사전 용도로 충분합니다

## [1순위. Introduction to Robotics: Mechanics and Control — J. J. Craig]
- 판·출판: 4th ed., Pearson, 2017
- 받쳐 주는 코드: `M2_kinematics_dynamics/` 전체, 특히 `runnable/` 패키지
- 추천 이유
  - 교안(12강)이 직접 인용하는 책이라 기호와 전개 순서가 교안과 가장 잘 맞음
  - D-H → FK → IK → Jacobian → 동역학 → 궤적이 이 저장소 13~15강 코드와 같은 순서
  - Physical AI에서 뒤에 나오는 모든 것(비전 좌표 변환, Sim2Real의 System ID)이 이 기초 위에 있음
- 먼저 읽을 곳
  - 2장 공간 기술과 변환 → `transforms.py`
  - 3장 순기구학 → `fk_chain.py`
  - 5장 Jacobian·특이점 → `jacobian.py`
  - 6장 동역학 → `arm_dynamics.py`
  - 7장 궤적 생성 → `trajectory.py`

## [2순위. Probabilistic Robotics — S. Thrun, W. Burgard, D. Fox]
- 판·출판: MIT Press, 2005
- 받쳐 주는 코드: `M6_slam_nav2/` (cuVSLAM·AMCL·Nav2)
- 추천 이유
  - SLAM 도구들은 설정만 바꾸면 돌아가지만, 왜 실패하는지는 이 책 없이 이해하기 어려움
  - 칼만 필터, 파티클 필터, SLAM을 하나의 베이즈 필터 틀로 설명해 도구가 바뀌어도 그대로 통함
  - 출간이 오래됐지만 이 분야의 표준 교과서 자리를 지키고 있음
- 먼저 읽을 곳
  - 2장 재귀적 상태 추정(베이즈 필터)
  - 3장 가우시안 필터(KF·EKF)
  - 4장 비모수 필터(파티클 필터)
  - 8장 Monte Carlo Localization → AMCL의 원리

## [3순위. ★ Understanding Deep Learning — S. J. D. Prince]
- 판·출판: MIT Press, 2023 (저자 공식 무료 PDF 공개)
- 받쳐 주는 코드: `M7_imitation_learning/` (BC·Diffusion Policy), `M4_3d_perception/` YOLO
- 추천 이유
  - CNN·Transformer·확산 모델을 한 권에서 같은 표기로 다루는 드문 최신 교과서
  - 그림이 많고 수식을 단계별로 풀어 줘, 혼자 읽기에 부담이 적음
  - 무료라 바로 시작할 수 있음
- 먼저 읽을 곳
  - 10장 합성곱 신경망 → 51강 CNN 정책
  - 12장 Transformer → 51강 Transformer 정책
  - 18장 확산 모델 → 52강 Diffusion Policy

## [읽는 순서]
- Craig 2~7장 → `runnable/`의 테스트와 데모를 직접 돌리며 확인
- Probabilistic Robotics 2~4·8장 → 모듈 ⑥ 실습 전에
- Understanding Deep Learning 10·12·18장 → 모듈 ⑦ 실습 전에
- 그 밖의 주제(제어, MCU, 카메라 기하, ROS 2, 실시간)는 막힐 때 `reference.md`에서 해당 책을 찾아보기
