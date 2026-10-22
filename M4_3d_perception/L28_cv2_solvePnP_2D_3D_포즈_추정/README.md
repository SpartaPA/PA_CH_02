# [28강. [실습] cv2.solvePnP 2D-3D 포즈 추정]
- 모듈: ④ 2D/3D 공간 인지 및 비전 AI
- 한 줄 요약: 정답 포즈를 아는 합성 장면으로 PnP 오차를 계량하는 벤치마크를 만들고, 이상치 오염 실험과 품질 게이트를 거쳐 실물 상자 포즈 추정기로 적용

## [핵심 개념]
- 합성 벤치마크: 정답 $(R_{true},t_{true})$로 3D 점을 투영해 2D 관측 생성 → 추정값과 정답의 차이를 직접 측정
  - 실험 변수: 노이즈 크기(px), 점 개수, 이상치 비율
- 관측 모델: $x_i=\pi(K(RX_i+t))+\epsilon_i$, $\epsilon_i\sim\mathcal N(0,\sigma^2)$
- 이상치 주입: 일부 픽셀을 이미지 전체(640×480) 균일 분포로 교체 → 오매칭 흉내
- 포즈 오차 지표
  - 회전 오차: $\Delta R=R_{est}R_{true}^\top$, $\theta=\arccos\frac{\mathrm{tr}(\Delta R)-1}{2}$ [deg]
  - 이동 오차: $\|t_{est}-t_{true}\|$ [m]
  - `np.clip(..., -1, 1)`: 수치 오차로 arccos 정의역 이탈 방지
- RANSAC + 품질 게이트: 성공 플래그만으로는 부족 → inlier 수·비율로 결과 신뢰 여부 판정
- 실물 적용: 물체 좌표계(원점·축)를 정의한 3D 모델 점 + 이미지 클릭 대응 → PnP
  - 상자 꼭짓점 8개 중 보이는 6~7개만 사용

## [파일별 내용]
- `01_pnp_bench.ipynb` — 원본 `src/pnp_bench.py` 핵심부
  - `make_scene(n_pts, R_true, t_true, K, noise_px=0.5, outlier_ratio=0.0)`
    - 물체 점: 한 변 0.2 m 정육면체 안 균일 분포 `(n_pts,3)` float32
    - `project_points`(23강 `project`의 배열 버전)로 투영 → 가우시안 노이즈 → 이상치 주입
    - 반환: `obj`(3D), `img`(2D) float32
  - `pose_error(rvec, tvec, R_true, t_true)`: `cv2.Rodrigues`로 회전행렬 변환 후 (각도 [deg], 거리 [m]) 반환
  - 빠진 맥락: 전역 `rng`(`np.random.default_rng`), `project_points` 정의, 실험 루프·그래프 코드
- `02_실험_3_RANSAC_오염_실험.ipynb` — 교안 4절 "실험 3" 발췌
  - `solvePnPRansac(obj, img, K, None, reprojectionError=3.0, iterationsCount=200, flags=SOLVEPNP_P3P)`
  - `gate`: `ok`이고 inlier가 `max(6, 0.4*N)`개 이상일 때만 결과 채택
  - 실험 1·2(노이즈·점 개수 실험) 코드는 이 폴더에 없음
- `03_실물_상자_포즈_추정기.ipynb` — 상자 모델 `BOX`: 밑면 중심을 원점으로 한 8개 꼭짓점 `(8,3)`
  - `W`·`D`·`H`(가로·세로·높이)는 실측값으로 정의 필요
  - 클릭 UI·인덱스 매핑·검증 단계는 주석으로만 제시

## [선수 지식·연결]
- 23강: `project()` → `project_points`로 재사용
- 24강: `solvePnPRansac`, P3P/EPnP 원리
- 20강: 실물 실험에 쓸 $K$·왜곡계수
- 29강: 2D 검출을 3D로 승격하는 다른 경로(바닥 평면 교차)와 비교

## [실행 전 준비]
- Python 3, `opencv-python`, NumPy, (그래프용) Matplotlib
- 실물 실험: 캘리브레이션된 카메라, 치수를 잰 상자, 꼭짓점 클릭용 `cv2.setMouseCallback` 등

## [확인 포인트]
- 기대 결과: 노이즈가 클수록·점이 적을수록 오차 증가, 이상치가 섞여도 RANSAC은 게이트 통과 범위에서 작은 오차 유지
- 흔한 실수
  - `t_true` 형상 `(3,)`와 `tvec` `(3,1)` 혼동 → `ravel()` 필요(코드에 반영됨)
  - 정답 포즈가 물체를 카메라 뒤에 두어 투영값이 무의미
  - 실물에서 클릭 순서와 `BOX` 인덱스 매핑 불일치 → 엉뚱한 포즈
- 점검 질문
  - 이상치 비율을 몇 %까지 올리면 게이트가 실패하기 시작하는가?
  - 물체 점 범위(±0.1 m)를 줄이면 같은 픽셀 노이즈에서 오차가 왜 커지는가?
  - 게이트 기준을 inlier 수가 아닌 재투영 오차 RMS로 바꾸면 어떤 장단점이 있는가?
