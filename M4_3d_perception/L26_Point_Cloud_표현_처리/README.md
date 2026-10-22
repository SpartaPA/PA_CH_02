# [26강. Point Cloud 표현·처리 (PCL/Open3D·필터·세그멘테이션)]
- 모듈: ④ 2D/3D 공간 인지 및 비전 AI
- 한 줄 요약: 순서 없는 3D 점 집합을 Open3D로 다루며 Voxel 다운샘플 → SOR 이상치 제거 → RANSAC 평면 추출 → DBSCAN 클러스터링의 표준 파이프라인 구성

## [핵심 개념]
- Point Cloud 표현
  - $N\times3$ 좌표 배열(선택적으로 색·법선 추가), 점 사이 순서·격자 없음
  - 이미지처럼 이웃 = 인접 인덱스가 아님 → KD-tree 등으로 공간 이웃 검색 필요
- Voxel 다운샘플
  - 공간을 한 변 $v$의 정육면체 격자로 나누고 칸마다 점들의 평균(중심) 1개로 대체
  - 점 수 감소 + 밀도 균일화 → 이후 단계 계산량 감소
- SOR(Statistical Outlier Removal)
  - 각 점의 $k$개 최근접 이웃 평균거리 $d_i$ 계산
  - 전체 $d_i$의 평균 $\mu$, 표준편차 $\sigma$에 대해 $d_i>\mu+\alpha\sigma$인 점 제거
  - 허공에 떠 있는 센서 노이즈 제거용
- RANSAC 평면 추출
  - 3점 무작위 추출 → 평면 $ax+by+cz+d=0$ 가설
  - 점-평면 거리 $\frac{|ax+by+cz+d|}{\sqrt{a^2+b^2+c^2}}$가 임계값 이내인 점을 inlier로 집계, 최다 합의 평면 채택
  - 테이블·바닥 제거 → 남은 점 = 물체 후보
- DBSCAN 클러스터링
  - 반경 `eps` 안에 이웃이 `min_points` 이상이면 핵심점, 핵심점끼리 연결된 덩어리 = 클러스터
  - 클러스터 수 사전 지정 불필요, 어느 클러스터에도 속하지 않으면 라벨 $-1$(노이즈)
- 파라미터 단위: 모두 점 좌표 단위(보통 m) → 센서 해상도·다운샘플 크기와 맞춰 설정

## [파일별 내용]
- `01_표현_순서_없는_점들의_집합.ipynb` — `(N,3)` ndarray `xyz`를 `o3d.utility.Vector3dVector`로 감싸 `PointCloud` 생성, `draw_geometries`로 시각화
  - 빠진 맥락: `xyz` 생성·로드 코드(예: `o3d.io.read_point_cloud` 또는 31강 역투영 결과)
- `02_필터_①_Voxel_다운샘플_점을_줄여야_시작된다.ipynb` — `voxel_down_sample(voxel_size=0.01)`: 1 cm 격자로 다운샘플 → `down`
- `03_필터_②_SOR_통계로_이상치_걷어내기.ipynb` — `remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)`
  - 반환: 정제된 클라우드 `clean`, 남은 점 인덱스 `idx`
- `04_평면_추출_RANSAC의_재등판.ipynb` — `segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)`
  - `plane`: 평면 계수 $[a,b,c,d]$, `inliers`: 평면 점 인덱스
  - `select_by_index(inliers)` → `table`, `invert=True` → `objects`
- `05_클러스터링_덩어리를_개체로.ipynb` — `objects.cluster_dbscan(eps=0.02, min_points=10)` → 점별 라벨 배열
  - 이후 클러스터별 중심·바운딩박스 계산은 주석으로만 제시(30강에서 구현)
- 파일 02~05는 앞 파일의 변수(`pcd`→`down`→`clean`→`objects`)를 이어 쓰는 연속 코드

## [선수 지식·연결]
- 24강: RANSAC 원리 → 평면 추출에 "재등판"
- 27·31강: RGBD 역투영으로 Point Cloud 생성 → 이 강의 입력
- 30강: 같은 파이프라인을 `segment_objects()`로 묶고 합성 정답 장면으로 단계별 계량

## [실행 전 준비]
- `pip install open3d`, NumPy
- `draw_geometries`는 GUI 창 필요(원격/헤드리스 환경에서는 동작하지 않을 수 있음)
- 시험용 점군: 직접 합성하거나 `.ply`/`.pcd` 파일

## [확인 포인트]
- 기대 결과: 단계마다 점 수 감소, 평면 제거 후 물체 덩어리만 남고 DBSCAN 라벨이 물체 개수만큼 생성
- 흔한 실수
  - `voxel_size`보다 `eps`가 작으면 다운샘플된 점끼리 이어지지 않아 클러스터가 잘게 쪼개짐
  - 테이블보다 벽·바닥이 더 크면 RANSAC이 엉뚱한 평면을 선택
  - `cluster_dbscan` 반환값이 리스트형 → `np.array`로 변환 후 `labels.max()` 사용
- 점검 질문
  - `std_ratio`를 1.0으로 낮추면 물체 가장자리 점은 어떻게 되는가?
  - Voxel 다운샘플을 SOR보다 먼저 하는 이유는?
  - 서로 맞닿은 두 물체는 DBSCAN으로 분리되는가?
