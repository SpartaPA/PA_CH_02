# [24강. PnP 심화 (EPnP·P3P)]
- 모듈: ④ 2D/3D 공간 인지 및 비전 AI
- 한 줄 요약: PnP 풀이법(P3P·EPnP)의 원리를 이해하고, 대응점에 이상치가 섞였을 때 `cv2.solvePnPRansac`으로 강건하게 포즈를 구하는 방법 습득

## [핵심 개념]
- PnP 문제: 물체 좌표계 3D 점 $\{X_i\}$와 그 픽셀 $\{x_i\}$의 대응, 그리고 $K$가 주어질 때 $[R|t]$ 추정
  - 목표: 재투영 오차 최소화 $\min_{R,t}\sum_i\|x_i-\pi(K(RX_i+t))\|^2$
  - 자유도 6(회전 3 + 이동 3), 점 하나당 식 2개 → 이론상 최소 3점
- P3P: 최소 3점으로 닫힌 형태 해 → 해가 최대 4개 → 4번째 점 등으로 모호성 해소
- EPnP: $n$개 점을 가상 제어점 4개의 가중합(무게중심 좌표)으로 표현 → 제어점의 카메라 좌표만 풀면 됨 → $O(n)$
- 반복 최적화(`SOLVEPNP_ITERATIVE`): Levenberg–Marquardt로 재투영 오차 최소화, 초기값에 민감
- 이상치(outlier): 잘못된 대응(오매칭)은 최소제곱 해를 크게 왜곡
- RANSAC
  - 최소 표본(P3P면 3~4점) 무작위 추출 → 가설 포즈 계산
  - 모든 점을 재투영해 오차가 임계값 이내인 점(inlier) 수 집계
  - 합의가 가장 큰 가설 채택, 필요 시 inlier 전체로 재추정
  - 필요 반복 수: $N\ge\frac{\log(1-p)}{\log(1-w^s)}$ ($w$: inlier 비율, $s$: 표본 크기, $p$: 성공 확률)
- `rvec`: Rodrigues 회전벡터(축 × 각도), `cv2.Rodrigues`로 $R$ 변환

## [파일별 내용]
- `01_이상치의_세계_RANSAC.ipynb` — 교안 3절 "이상치의 세계" 코드 한 줄 발췌
  - `cv2.solvePnPRansac(obj_pts, img_pts, K, dist, ...)`
    - `obj_pts`: (N,3) float32 물체 좌표, `img_pts`: (N,2) float32 픽셀
    - `dist`: 왜곡계수(없으면 `None`)
    - `reprojectionError=3.0`: inlier 판정 임계값 [px]
    - `iterationsCount=100`: RANSAC 반복 횟수 상한
    - `flags=cv2.SOLVEPNP_P3P`: 최소 표본 풀이기로 P3P 사용
  - 반환: `ok`(성공 여부), `rvec`, `tvec`(물체 → 카메라 변환), `inliers`(inlier 인덱스 배열)
  - 빠진 맥락: `import cv2`, 대응점·`K`·`dist` 준비 코드 없음

## [선수 지식·연결]
- 18강: PnP 개념, `cv2.solvePnP` 기본 사용
- 23강: `project()` → 재투영 오차 계산의 기반
- 26강: 같은 RANSAC 아이디어를 평면 추출(`segment_plane`)에 재사용
- 28강: 이 함수를 합성 벤치마크와 오염 실험, 실물 상자 포즈 추정기로 확장

## [실행 전 준비]
- Python 3, `opencv-python`, NumPy
- 캘리브레이션된 $K$·왜곡계수(20강 결과) 또는 합성 데이터

## [확인 포인트]
- 기대 결과: 이상치가 있어도 `ok=True`, `inliers`에 정상 대응점 대부분 포함
- 흔한 실수
  - 입력 배열 dtype을 float64/int로 넘겨 오류 → `float32` 권장
  - `reprojectionError`를 너무 크게 잡아 이상치가 inlier로 섞임, 너무 작게 잡아 노이즈 있는 정상점까지 탈락
  - `tvec` 단위는 `obj_pts` 단위를 따름(m로 넣으면 m)
- 점검 질문
  - inlier 비율 50%, 표본 4점, 성공 확률 99%면 반복 수는 대략 몇 번 필요한가?
  - P3P가 해를 여러 개 내는 이유와 RANSAC 안에서 이를 고르는 방법은?
  - 점이 모두 한 평면 위에 있을 때 고려할 플래그(`SOLVEPNP_IPPE` 등)는?
