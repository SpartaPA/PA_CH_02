# [runnable — 13~15강 실행·테스트 패키지]
- 모듈: ② 로봇 기구학 및 동역학
- 한 줄 요약: 13~15강 교안 코드(FK·Jacobian·궤적·동역학)를 실행 가능한 노트북 모듈로 묶고, 테스트와 데모로 결과까지 재현하는 패키지

## [구성]
- `src/` — 함수·클래스 정의(재사용 도구), 의존 순서 `transforms` → `fk_chain` → `jacobian`
- `tests/` — 교안의 pytest 테스트를 노트북으로, 마지막 셀이 직접 돌려 `N passed` 출력
- `demos/` — 13~15강 실험 절차를 실행하고 그림을 `demos/out/`에 저장
- 불러오기: `%run -i ../src/<모듈>.ipynb` (원래의 `from src.x import ...` 대체)

## [src 함수별 내용]
- `transforms.ipynb` (13강)
  - `rot_z(theta)`, `rot_x(alpha)`, `trans(x,y,z)`: 4×4 동차변환 블록
  - `dh_transform(theta, d, a, alpha)`: $R_z(\theta)T_z(d)T_x(a)R_x(\alpha)$
- `fk_chain.ipynb` (13강)
  - `PlanarArm(link_lengths)`: `fk_all(thetas)` → 링크별 $T_0^{\,i}$ 목록, `fk(thetas)` → 손끝 $(x,y)$
  - `Arm3D(PlanarArm)`: 허리 회전(D-H 행 $d=0.15,\alpha=\pi/2$) + 평면 2링크, `fk()`를 $(x,y,z)$ 반환으로 재정의(보강)
  - `dh_transform`이 없으면 `transforms.ipynb`를 먼저 실행
- `jacobian.ipynb` (14강)
  - `jacobian_planar(L, thetas)`: 해석적 2×N Jacobian
  - `jacobian_numeric(fk, thetas, eps=1e-6)`: 중앙차분 검증자
  - `singularity_metrics(J)`: 조작성 $w$, $\sigma_{\min}$, 조건수
  - `dls(J, xdot, lam=0.05)`: $J^\top(JJ^\top+\lambda^2I)^{-1}\dot x$
  - `adaptive_lambda(J)`: $\sigma_{\min}\le0.05$일 때만 $\lambda=0.1(1-\sigma_{\min}/0.05)$
- `trajectory.ipynb` (15강)
  - `quintic(theta0, thetaf, T)` → `eval(t)`가 `(pos, vel, acc)` 반환, 정지→정지 5차 궤적
- `arm_dynamics.ipynb` (15강, 교안 생략부 보강)
  - `TwoLinkDynamics(m=(1.0,0.8), L=(0.3,0.2), g=9.81)`: 링크 끝 점질량, 수직 평면 2링크, θ는 수평 기준
  - `M(th)`: $m_{11}=m_1L_1^2+m_2(L_1^2+L_2^2+2L_1L_2c_2)$, $m_{12}=m_2(L_2^2+L_1L_2c_2)$, $m_{22}=m_2L_2^2$
  - `C(th, thd)`: $h=m_2L_1L_2s_2$ 기반 코리올리·원심 행렬
  - `gvec(th)`: $g_2=m_2gL_2c_{12}$, $g_1=(m_1+m_2)gL_1c_1+g_2$ (수평일 때 최대)
  - `energy()`: 운동에너지 $\tfrac12\dot\theta^\top M\dot\theta$ + 위치에너지
  - `step(tau, dt)`: 교안 원문 semi-implicit Euler, `step_rk4(tau, dt)`: 보강한 RK4

## [tests]
- `test_fk.ipynb` — 기지 자세 5건(parametrize) + 3링크 누적각 공식 비교 1건, `atol=1e-12`
- `test_jacobian.ipynb` — 해석해 = 수치해 3건(`atol=1e-6`) + 펴진 자세(θ2=0) 특이점 탐지 1건(조작성 < 1e-6, σ_min < 1e-12)
- `test_dynamics.ipynb` — 4건
  - 에너지 보존: RK4, 5 s 자유 진동, 상대오차 < 1e-6(원문은 Euler·1e-2로 불통과)
  - $M$ 대칭·양의 정부호: θ2를 $-\pi\sim\pi$ 13점에서 검사
  - 중력 보상 자세 유지: 수평 자세에서 $\tau=g(\theta)$이면 1000스텝 후에도 θ=0
  - Quintic 경계조건: 양 끝 위치·속도·가속도
- 마지막 셀: `test_*` 함수를 찾아 `pytest.mark.parametrize` 케이스까지 전개해 직접 호출(`pytest` 실행기 없이 동작, 데코레이터 때문에 `pytest` import는 필요)

## [demos와 결과]
- `demo_fk_workspace.ipynb` (13강) → `out/fk_workspace.png`
  - 왼쪽: 세 자세 그림, 오른쪽: 2만 점 몬테카를로 작업 공간
  - 결과: 도달 반경 0.100~0.500 m(이론 $|L_1-L_2|\sim L_1+L_2$)
- `demo_singularity.ipynb` (14강) → `out/singularity.png`
  - 초기 `TH0=[0.3,-0.8]`(반경 ≈0.46 m), 손끝을 반경 방향 2 cm/s로 밀어 약 2 s 뒤 경계 특이점 도달, `dt=0.01`·400스텝
  - 결과: 최대 관절속도 pinv 236.5 rad/s(폭주) vs 가변 λ DLS 0.39 rad/s, 아래 그래프는 조작성 $w$ 변화
- `demo_tracking.ipynb` (15강) → `out/tracking.png`
  - 목표 `thf=[π/3, π/4]`, `T=1.5` s, 시뮬 3 s, `dt=1e-3`, `Kp=[40,20]`, `Ki=[10,5]`, `Kd=[4,1.5]`
  - 계단/Quintic × PID/PID+g 4조합, θ1 궤적 비교
  - 결과(RMS, rad): 계단+PID 0.165 · 계단+PID+g 0.158 · Quintic+PID 0.072 · Quintic+PID+g 0.0099

## [실행 전 준비]
- `pip install numpy scipy matplotlib pytest jupyterlab`
- 노트북 작업 디렉터리가 해당 노트북 폴더여야 `../src/` 상대경로가 맞음
- 일괄 실행: `jupyter nbconvert --to notebook --execute --inplace M2_kinematics_dynamics/runnable/*/*.ipynb`

## [확인 포인트]
- 기대 결과: 테스트 합계 14 passed(FK 6, Jacobian 4, 동역학 4), 데모 그림 3장 생성
- 흔한 실수
  - `%run -i` 셀을 건너뛰고 아래 셀 실행 → `NameError`
  - 다른 폴더에서 커널 시작 → `../src` 경로 오류
- 점검 질문
  - 에너지 테스트를 `step`(Euler)으로 되돌리면 실패하는 이유는 모델인가 적분기인가?
  - 계단 기준 RMS는 도달 불가능한 순간 점프까지 오차로 셈 → Quintic과의 비교에서 이를 어떻게 해석할까?
