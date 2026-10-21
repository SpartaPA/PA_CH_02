# Reference — 핵심 참고 서적

분야마다 한 권만 골랐습니다. 교안의 모듈 순서대로 정리했습니다. ★는 저자가 공식적으로 무료 PDF를 공개한 책입니다.

| # | 서적 | 대응 모듈 | 고른 이유 |
|---|---|---|---|
| 1 | ★ K. J. Åström, R. M. Murray, *Feedback Systems: An Introduction for Scientists and Engineers*, 2nd ed., Princeton University Press, 2021 | ① 1~3·7강 | 전달함수, 극점과 안정성, PID와 anti-windup을 수식 부담 적게 설명합니다. 공식 무료 공개본이 있습니다. |
| 2 | J. Yiu, *The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors*, 3rd ed., Newnes, 2014 | ① 4~8강 | 메모리맵, NVIC 인터럽트, 타이머 등 STM32/OpenCR 펌웨어의 바탕을 다루는 표준 레퍼런스입니다. |
| 3 | J. J. Craig, *Introduction to Robotics: Mechanics and Control*, 4th ed., Pearson, 2017 | ② 9~15강 | D-H, FK/IK, Jacobian·특이점, 동역학, 궤적 생성을 순서대로 다룹니다. 교안(12강)이 직접 인용하는 책입니다. |
| 4 | R. Hartley, A. Zisserman, *Multiple View Geometry in Computer Vision*, 2nd ed., Cambridge University Press, 2004 | ③④ 17~18·20·23~24·27강 | 핀홀 모델, 캘리브레이션, PnP, RANSAC, 스테레오 기하의 표준 교과서입니다. |
| 5 | S. Thrun, W. Burgard, D. Fox, *Probabilistic Robotics*, MIT Press, 2005 | ⑥ 37~40강 | 베이즈 필터, EKF, Particle Filter(AMCL), SLAM과 occupancy grid를 하나의 확률 틀로 설명합니다. |
| 6 | ★ S. J. D. Prince, *Understanding Deep Learning*, MIT Press, 2023 | ④ 25강, ⑦ 47~52강 | CNN, Transformer, 확산 모델(Diffusion)을 최신 관점에서 한 권으로 다룹니다. 공식 무료 공개본이 있습니다. |
| 7 | F. Martín Rico, *A Concise Introduction to Robot Programming with ROS2*, CRC Press, 2022 | ①⑥⑨ ROS 2 실습 전반 | rclpy/rclcpp 노드, TF, Behavior Tree, Nav2를 실습 중심으로 설명합니다. |
| 8 | G. C. Buttazzo, *Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications*, 3rd ed., Springer, 2011 | ⑨ 66·69강 | deadline, jitter, 스케줄 가능성 분석 등 실시간 제어 루프 설계의 이론적 바탕입니다. |

## 책이 아니라 논문으로 보충할 주제

모듈 ⑦·⑧의 최신 주제(DAgger, Diffusion Policy, Domain Randomization, Sim2Real)는 아직 표준 교과서가 없습니다. 아래 원 논문을 함께 보는 것이 가장 정확합니다.

- S. Ross, G. Gordon, D. Bagnell, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning" (DAgger), AISTATS 2011
- C. Chi et al., "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion", RSS 2023
- J. Tobin et al., "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World", IROS 2017
