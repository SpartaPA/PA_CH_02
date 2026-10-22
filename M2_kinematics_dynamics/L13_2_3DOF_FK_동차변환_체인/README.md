# [13강. [실습] 2~3DOF FK 동차변환 체인]
- 모듈: ② 로봇 기구학 및 동역학
- 한 줄 요약: 4×4 동차변환 블록과 D-H 한 행 변환을 만들고, 이를 곱해 2~3링크 팔의 순기구학(FK)을 계산·테스트·시각화(자세, 작업 공간, 3D 확장)

## [핵심 개념]
- 동차변환 $T=\begin{bmatrix}R&p\\0&1\end{bmatrix}$
  - 회전 $R$과 평행이동 $p$를 한 행렬로 → 좌표계 변환을 행렬 곱으로 연결
  - 기본 블록: $R_z(\theta)$, $R_x(\alpha)$, $T(x,y,z)$
- Standard D-H 한 행 $(\theta,d,a,\alpha)$
  - $T_{i-1}^{\,i}=R_z(\theta)\,T_z(d)\,T_x(a)\,R_x(\alpha)$
  - 회전 관절은 $\theta$가 변수, 나머지는 링크 상수
- FK 체인: $T_0^{\,n}=\prod_{i=1}^{n}T_{i-1}^{\,i}$, 손끝 위치 = $T_0^{\,n}$의 4열 위 3성분
- 평면 2링크 닫힌 형태
  - $x=L_1c_1+L_2c_{12},\;y=L_1s_1+L_2s_{12}$ ($c_{12}=\cos(\theta_1+\theta_2)$)
  - $n$링크 일반형: $x=\sum_i L_i\cos\big(\sum_{k\le i}\theta_k\big)$ → 3DOF 테스트의 `np.cumsum`
- 작업 공간: 관절 각을 무작위로 뽑아 FK → 도달 가능한 점 집합
  - 2링크 평면 팔은 반경 $|L_1-L_2|\sim L_1+L_2$의 고리(annulus), 여기선 0.1~0.5 m
- 테스트로 잠그기: 손으로 검산한 기지 자세(9강 검산표)를 `pytest`로 자동 비교 → 이후 수정이 FK를 깨뜨리지 않음 보장

## [파일별 내용]
- `01_transforms.ipynb` — 원본 `src/transforms.py`: `rot_z(theta)`, `rot_x(alpha)`, `trans(x,y,z)`가 4×4 행렬 반환
- `02_기본_변환_블록_만들기.ipynb` — `dh_transform(theta, d, a, alpha)` = 네 블록의 곱(01과 같은 모듈에 들어갈 함수)
- `03_fk_chain.ipynb` — 원본 `src/fk_chain.py`: `PlanarArm`
  - `__init__(link_lengths)`: `self.L` 링크 길이 목록
  - `fk_all(thetas)`: 각 링크 끝의 $T_0^{\,i}$ 목록(시각화용), 각 링크를 D-H 행 $(\theta_i,0,L_i,0)$으로 표현
  - `fk(thetas)`: 마지막 변환의 $(x,y)$
  - docstring의 `dh_rows`는 실제 인자명(`link_lengths`)과 불일치(원문 그대로)
  - `from .transforms import ...` 상대 import → 패키지 구조 전제
- `04_FK_체인_로봇을_데이터로_표현하기.ipynb` — `PlanarArm([0.3, 0.2])`로 `fk([0,0])=[0.5,0]`, `fk([π/2,0])=[0,0.5]` 확인
- `05_test_fk.ipynb` — 원본 `tests/test_fk.py`
  - `CASES` 5개 기지 자세를 `@pytest.mark.parametrize`로 `atol=1e-12` 비교
  - `test_fk_3dof_matches_formula`: 3링크 FK를 누적각 닫힌 형태와 비교
- `06_자세_그리기.ipynb` — `draw_arm(ax, arm, thetas)`: 원점 + 각 관절 위치를 선·점으로 그림
- `07_작업_공간_FK를_몬테카를로로.ipynb` — 2만 개 무작위 관절각 $[-\pi,\pi]^2$ → FK 산점도
  - 루프 기반(느림), 교안 과제: 벡터화
  - `arm`, `plt`는 앞 셀에서 정의된 것 전제
- `08_3D로_확장.ipynb` — `Arm3D(PlanarArm)`: 허리 회전 행 `dh_transform(θ0, 0.15, 0, π/2)` 추가 후 평면 2링크
  - 원문은 `fk()`를 재정의하지 않아 부모의 $(x,y)$만 반환 → `runnable/`에서 $(x,y,z)$로 보강

## [선수 지식·연결]
- 9강(이론): D-H 규약, 손 검산표
- `runnable/src/transforms.ipynb`, `fk_chain.ipynb`: 이 강의 코드의 실행 가능한 판
- 14강: `PlanarArm.fk`가 수치 Jacobian의 입력, `L`이 해석적 Jacobian의 입력
- 10강 IK: FK + Jacobian 반복으로 역문제 풀이

## [실행 전 준비]
- `numpy`, `matplotlib`, `pytest`
- 강의 폴더 노트북은 발췌라 단독 실행 시 정의 누락 → `runnable/` 노트북 사용 권장

## [확인 포인트]
- 기대 결과: 테스트 6건 통과(기지 자세 5 + 3DOF 1), 작업 공간 반경 0.100~0.500 m
- 흔한 실수
  - `rot_z @ trans` 곱 순서를 바꾸면 다른 변환(회전된 축 기준 이동 vs 고정 축 기준)
  - 도(°)와 라디안 혼용
- 점검 질문
  - $L_1=L_2$이면 작업 공간 모양은 어떻게 바뀌는가?
  - `Arm3D`에서 $\alpha=\pi/2$ 행이 하는 역할은?
