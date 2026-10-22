# [15강. [실습] Quintic 궤적 생성 + PID 튜닝]
- 모듈: ② 로봇 기구학 및 동역학
- 한 줄 요약: 정지→정지 5차(Quintic) 궤적을 만들고, 12강 동역학으로 만든 2링크 팔 시뮬레이터 위에서 계단 vs Quintic, PID vs PID+중력 보상의 추종 성능을 비교

## [핵심 개념]
- 왜 5차인가
  - 경계조건 6개: $\theta(0),\dot\theta(0),\ddot\theta(0),\theta(T),\dot\theta(T),\ddot\theta(T)$ → 미지 계수 6개 다항식
  - 정지→정지 해: $\theta(t)=\theta_0+\Delta\left(10\tfrac{t^3}{T^3}-15\tfrac{t^4}{T^4}+6\tfrac{t^5}{T^5}\right)$, $\Delta=\theta_f-\theta_0$
  - 최대 속도 $1.875\,\Delta/T$ ($t=T/2$)
  - 양 끝 가속도 0 → 계단 입력 대비 토크 충격·오버슈트 감소
- 로봇팔 동역학 $M(\theta)\ddot\theta+C(\theta,\dot\theta)\dot\theta+g(\theta)=\tau$
  - $M$: 대칭·양의 정부호 관성 행렬, $\cos\theta_2$ 항 때문에 자세 의존
  - $C$: 코리올리·원심, $g$: 중력 토크
  - 시뮬레이션: $\ddot\theta=M^{-1}(\tau-C\dot\theta-g)$를 적분
- 수치 적분
  - semi-implicit Euler: 속도 먼저 갱신 → 갱신된 속도로 위치 갱신
  - 큰 진폭 자유 진동에서 에너지 누설이 큼 → 검증은 RK4로(루트 README [원문 대비 보강·수정 사항])
- 관절 PID + 중력 보상
  - $\tau=K_p e+K_d\dot e+K_i\!\int e\,dt+\hat g(\theta)$
  - 아는 힘(중력)은 피드포워드, 피드백은 모델 오차만 담당 → 적분이 중력을 떠안을 필요가 없어 지연·오버슈트 감소
  - 튜닝은 관성이 가장 큰 자세(팔꿈치 펴짐)에서

## [파일별 내용]
- `01_trajectory.ipynb` — 원본 `src/trajectory.py`: `quintic(theta0, thetaf, T)`
  - 계수 `a3, a4, a5`를 미리 계산하고 `eval(t)` 클로저 반환
  - `eval(t)` → `(pos, vel, acc)`, `np.clip`으로 $[0,T]$ 밖은 끝값 유지
  - 내부 함수 이름 `eval`이 내장 함수를 가림(동작엔 무관)
- `02_arm_dynamics.ipynb` — 원본 `src/arm_dynamics.py` 핵심부: `TwoLinkDynamics`
  - 기본값 `m=(1.0, 0.8)`, `L=(0.3, 0.2)`, `g=9.81`
  - `M`, `C`, `gvec`, `__init__` 본문이 `...`로 생략 → 이대로는 실행 불가
  - `step(tau, dt=1e-3)`: `np.linalg.solve`로 $\ddot\theta$ 계산 후 semi-implicit Euler
- `03_시뮬레이터_12강_동역학을_코드로.ipynb` — `test_energy_conservation_without_damping`
  - 초기자세 (0.3, 0.5) rad, 토크 0으로 5000스텝(5 s) 후 에너지 상대오차 < 1e-2 기대
  - 원문 클래스에 없는 `sim.energy()` 호출, 오일러로는 약 25% 누설로 불통과 → `runnable/`에서 `energy()`·`step_rk4()` 추가로 수정
- `04_추종_실험_계단_vs_Quintic_PID_vs_PID_중력_보상.ipynb` — 관절별 PID 토크 한 줄 + `tau += sim.gvec(th)`(중력 보상 켜기)
  - 발췌: 기준 궤적 생성, 적분 `integ` 누적, 시뮬레이션 루프는 `runnable/demos/demo_tracking.ipynb`에 있음

## [선수 지식·연결]
- 12강(이론): 라그랑주 동역학, $M,C,g$ 유도
- 3·7강: 이산 PID와 anti-windup(여기선 포화 없음)
- 13강 FK와 같은 링크 길이(0.3, 0.2)
- 1강: 오버슈트·정착 개념으로 추종 그래프 해석

## [실행 전 준비]
- `numpy`, `matplotlib`, `pytest`
- 강의 폴더 코드는 생략(`...`)이 있어 단독 실행 불가 → `runnable/src/arm_dynamics.ipynb`, `runnable/tests/test_dynamics.ipynb`, `runnable/demos/demo_tracking.ipynb` 사용

## [확인 포인트]
- 기대 결과(RMS 추종 오차, rad): 계단+PID 0.165 · 계단+PID+g 0.158 · Quintic+PID 0.072 · Quintic+PID+g 0.0099
  - Quintic과 중력 보상을 함께 쓸 때 효과가 가장 큼
- 흔한 실수
  - `dt`를 키우면 Euler 적분이 불안정해져 결과가 발산
  - 중력 보상에 모델 $g$를 그대로 쓰면 "완벽한 모델" 가정 → 실물에선 $\hat g$ 오차가 남음
- 점검 질문
  - $T$를 줄이면 최대 속도·가속도와 필요 토크는 어떻게 변하는가?
  - 중력 보상 없이 $K_i$만으로 같은 성능을 내려면 무엇을 감수해야 하는가?
