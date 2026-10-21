# [Reference — 핵심 참고 서적]
- 분야마다 한 권만 선정, 교안의 모듈 순서대로 정리
- ★ = 저자가 공식적으로 무료 PDF를 공개한 책

## [1. ★ Feedback Systems: An Introduction for Scientists and Engineers]
- 저자: K. J. Åström, R. M. Murray
- 판·출판: 2nd ed., Princeton University Press, 2021
- 대응 모듈: ① 1~3·7강
- 선정 이유: 전달함수, 극점과 안정성, PID와 anti-windup을 수식 부담 적게 설명, 공식 무료 공개본 있음

## [2. The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors]
- 저자: J. Yiu
- 판·출판: 3rd ed., Newnes, 2014
- 대응 모듈: ① 4~8강
- 선정 이유: 메모리맵, NVIC 인터럽트, 타이머 등 STM32/OpenCR 펌웨어의 바탕을 다루는 표준 레퍼런스

## [3. Introduction to Robotics: Mechanics and Control]
- 저자: J. J. Craig
- 판·출판: 4th ed., Pearson, 2017
- 대응 모듈: ② 9~15강
- 선정 이유: D-H, FK/IK, Jacobian·특이점, 동역학, 궤적 생성을 순서대로 다룸, 교안(12강)이 직접 인용하는 책

## [4. Multiple View Geometry in Computer Vision]
- 저자: R. Hartley, A. Zisserman
- 판·출판: 2nd ed., Cambridge University Press, 2004
- 대응 모듈: ③④ 17~18·20·23~24·27강
- 선정 이유: 핀홀 모델, 캘리브레이션, PnP, RANSAC, 스테레오 기하의 표준 교과서

## [5. Probabilistic Robotics]
- 저자: S. Thrun, W. Burgard, D. Fox
- 판·출판: MIT Press, 2005
- 대응 모듈: ⑥ 37~40강
- 선정 이유: 베이즈 필터, EKF, Particle Filter(AMCL), SLAM과 occupancy grid를 하나의 확률 틀로 설명

## [6. ★ Understanding Deep Learning]
- 저자: S. J. D. Prince
- 판·출판: MIT Press, 2023
- 대응 모듈: ④ 25강, ⑦ 47~52강
- 선정 이유: CNN, Transformer, 확산 모델(Diffusion)을 최신 관점에서 한 권으로 다룸, 공식 무료 공개본 있음

## [7. A Concise Introduction to Robot Programming with ROS2]
- 저자: F. Martín Rico
- 판·출판: CRC Press, 2022
- 대응 모듈: ①⑥⑨ ROS 2 실습 전반
- 선정 이유: rclpy/rclcpp 노드, TF, Behavior Tree, Nav2를 실습 중심으로 설명

## [8. Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications]
- 저자: G. C. Buttazzo
- 판·출판: 3rd ed., Springer, 2011
- 대응 모듈: ⑨ 66·69강
- 선정 이유: deadline, jitter, 스케줄 가능성 분석 등 실시간 제어 루프 설계의 이론적 바탕

## [책이 아니라 논문으로 보충할 주제]
- 모듈 ⑦·⑧의 최신 주제(DAgger, Diffusion Policy, Domain Randomization, Sim2Real)는 아직 표준 교과서가 없어 원 논문을 함께 보는 것이 가장 정확
- DAgger: S. Ross, G. Gordon, D. Bagnell, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning", AISTATS 2011
- Diffusion Policy: C. Chi et al., "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion", RSS 2023
- Domain Randomization: J. Tobin et al., "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World", IROS 2017
