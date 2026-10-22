# [14강. [실습] Jacobian 속도 변환·특이점 탐지]
- 모듈: ② 로봇 기구학 및 동역학
- 한 줄 요약: 평면 팔의 해석적 Jacobian을 구현해 수치 미분으로 교차 검증하고, 속도 변환(정·역방향)과 특이점 지표, pinv 대 DLS 특이점 통과 실험까지 수행

## [핵심 개념]
- Jacobian: $\dot x=J(\theta)\dot\theta$, $J_{ij}=\partial x_i/\partial\theta_j$
- 평면 회전 팔 해석해
  - $j$열 = $j$번째 관절 이후 링크 벡터 합 $r_j$를 90° 회전: $J_{:,j}=\big(-\sum_{k\ge j}L_k s_{1..k},\;\sum_{k\ge j}L_k c_{1..k}\big)$
  - 2링크: $\det J=L_1L_2\sin\theta_2$ → $\theta_2=0,\pi$(완전히 펴짐·접힘)에서 특이
- 수치 미분(검증자): 중앙차분 $\frac{f(\theta+\epsilon e_j)-f(\theta-\epsilon e_j)}{2\epsilon}$, 오차 $O(\epsilon^2)$
- 속도 역변환(속도 IK)
  - 의사역행렬 $\dot\theta=J^{+}\dot x$, SVD 관점 $J^{+}=V\Sigma^{-1}U^\top$
  - $\sigma_{\min}\to0$이면 $1/\sigma_{\min}$이 폭주 → 관절 속도 발산
- 특이점 지표
  - 조작성 $w=\sqrt{\det JJ^\top}=\prod\sigma_i$
  - 최소 특이값 $\sigma_{\min}$, 조건수 $\kappa=\sigma_{\max}/\sigma_{\min}$
- Damped Least Squares
  - $\dot\theta=J^\top(JJ^\top+\lambda^2I)^{-1}\dot x$ → 각 방향 이득 $\sigma/(\sigma^2+\lambda^2)$로 상한
  - 대가: 특이점 근처에서 손끝 추종 오차 허용
  - 가변 $\lambda$: $\sigma_{\min}>0.05$이면 0, 이하에선 $0.1(1-\sigma_{\min}/0.05)$ → 평소엔 정확, 특이점 근처만 감쇠

## [파일별 내용]
- `01_jacobian.ipynb` — 원본 `src/jacobian.py`: `jacobian_planar(L, thetas)` → 2×N 행렬, `np.cumsum`으로 누적각
- `02_수치_미분_Jacobian_검증자.ipynb` — `jacobian_numeric(fk, thetas, eps=1e-6)`: 임의 FK 함수에 대한 중앙차분 Jacobian
- `03_test_jacobian.ipynb` — 원본 `tests/test_jacobian.py`: 3개 자세에서 해석해 = 수치해(`atol=1e-6`)
  - 발췌: `import`(numpy, pytest, `PlanarArm`, 두 Jacobian 함수) 생략
- `04_속도_변환_정방향과_역방향.ipynb` — `xdot = J @ thdot`, `thdot = np.linalg.pinv(J) @ xdot_desired`
  - `arm`, `th`, `thdot`, `xdot_desired`는 맥락에서 정의된다는 전제
- `05_특이점_탐지_지표를_코드로.ipynb` — `singularity_metrics(J)` → `manipulability`, `sigma_min`, `condition`(σ_min=0이면 `inf`)
  - `max(det, 0.0)`: 부동소수 음수 잔차 방지
- `06_특이점_통과_실험_폭주를_눈으로.ipynb` — (가) 순정 `pinv` vs (나) `dls(J, xdot, lam=0.05)`
  - `np.linalg.solve`로 역행렬 대신 선형계 풀이
- `07_특이점_통과_실험_폭주를_눈으로.ipynb` — 지표 기반 가변 `lam` 두 줄
  - `runnable/src/jacobian.ipynb`에서 `adaptive_lambda(J)` 함수로 정리됨

## [선수 지식·연결]
- 11강(이론): Jacobian 정의, 특이점의 기하학적 의미
- 13강: `PlanarArm`(`fk`, `L`)을 그대로 사용
- 10강 IK: Newton–Raphson $\theta\leftarrow\theta+J^{+}(x^\*-f(\theta))$이 이 Jacobian 재사용
- 선형대수: SVD, 의사역행렬

## [실행 전 준비]
- `numpy`, `matplotlib`, `pytest`
- 실행은 `runnable/tests/test_jacobian.ipynb`, `runnable/demos/demo_singularity.ipynb` 사용 권장

## [확인 포인트]
- 기대 결과: 교차 검증 3건 + 특이점 탐지 1건 통과, 데모 최대 관절속도 pinv 236.5 rad/s vs DLS 0.39 rad/s
- 흔한 실수
  - 수치 미분 `eps`를 너무 작게(예: 1e-12) → 반올림 오차로 오히려 부정확
  - `det(JJ^T)`의 제곱근은 0 근처에서 잔차가 커 보임 → 허용치를 넉넉히(1e-6)
- 점검 질문
  - 팔을 쭉 편 자세에서 손끝이 움직일 수 없는 방향은 어디인가?
  - $\lambda$를 크게 할수록 무엇을 얻고 무엇을 잃는가?
