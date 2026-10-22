# [30강. [실습] Point Cloud 필터링(Voxel/SOR) + RANSAC 평면·클러스터링]
- 모듈: ④ 2D/3D 공간 인지 및 비전 AI
- 한 줄 요약: 정답 라벨이 있는 합성 테이블 장면을 만들고, 26강 파이프라인을 `segment_objects()`로 조립해 단계마다 점 수·시간을 계량한 뒤 실데이터에 적용·시각화

## [핵심 개념]
- 정답 있는 실험대: 물체 위치·크기를 알고 만든 장면 → 검출 결과와 직접 비교(개수, 중심 오차, 크기 오차)
- 장면 구성: 테이블 평면 + 물체 3개 + 허공 노이즈 → 각각 RANSAC·DBSCAN·SOR가 처리할 대상
- 단계별 계량(instrumentation): 각 단계 후 점 수·누적 시간 기록 → 병목·과도한 제거 단계 파악
- 파이프라인: Voxel → SOR → RANSAC 평면 제거 → DBSCAN → 클러스터별 AABB
- AABB(Axis-Aligned Bounding Box)
  - 축 정렬 최소·최대 좌표 상자, 중심 $c=\frac{p_{min}+p_{max}}{2}$, 크기 $p_{max}-p_{min}$
  - 회전된 물체에서는 실제보다 크게 나옴(OBB와 차이)
- 파라미터 상호작용: `eps`는 `voxel`보다 충분히 커야 다운샘플된 점이 한 덩어리로 이어짐(여기서는 0.03 vs 0.01), `min_pts`는 남은 노이즈 덩어리 제거 역할
- 실데이터와 합성 데이터 차이: 가려짐(한쪽 면만 관측), 깊이 노이즈, 비균일 밀도

## [파일별 내용]
- `01_synth_scene.ipynb` — 원본 `src/synth_scene.py`, `make_table_scene(n_noise=300, seed=0)`
  - 테이블: 2.0×1.2 m, 2만 점, $z=0$
  - 물체 3개: `(center, size)` 지정, 각 4000점(`sample_box`), 정답 `truth` 리스트에 기록
  - 허공 노이즈: $[-1,1]\times[-0.6,0.6]\times[0,0.5]$ 균일 300점
  - 반환: `(N,3)` 점 배열, 정답 dict 리스트
  - 빠진 맥락: `sample_plane`, `sample_box` 정의, `import numpy as np`
  - 주의: 주석의 "원기등"은 원기둥 의미이나 코드는 `sample_box`로 생성(상자 형태)
- `02_segment.ipynb` — 원본 `src/segment.py`, `segment_objects(pcd, voxel=0.01, sor_k=20, sor_std=2.0, plane_dist=0.01, eps=0.03, min_pts=30)`
  - 단계마다 `log[...] = stat(..., t0)` 기록(`stat`은 점 수·경과 시간 집계 헬퍼로 추정, 정의 없음)
  - 라벨 `0..max`마다 점을 골라 AABB 중심·크기·점 수를 dict로 저장, 노이즈(−1)는 제외
  - 반환: 물체 후보 리스트 `out`, 단계 로그 `log`
  - 빠진 맥락: `import time`, `numpy`, `open3d`, `stat`
- `03_실데이터_적용과_시각화.ipynb` — 테이블은 회색, 클러스터는 `colorize`로 색 구분, `aabb_lineset`으로 상자 선 표시해 `draw_geometries`
  - `table`·`clusters`·`colorize`·`aabb_lineset`은 정의 없음 → 앞 단계 결과와 헬퍼를 직접 작성

## [선수 지식·연결]
- 26강: Voxel·SOR·RANSAC 평면·DBSCAN 각각의 원리와 Open3D 호출
- 28강: 정답 있는 합성 벤치마크라는 같은 실험 방식
- 31강: `segment_objects`를 검출 박스 ROI 클라우드에 재사용

## [실행 전 준비]
- `open3d`, NumPy
- 합성 점 배열 → `o3d.geometry.PointCloud`로 변환 후 `segment_objects`에 입력
- 실데이터: `.ply`/`.pcd` 파일 또는 31강 RGBD 역투영 결과, 시각화는 GUI 필요

## [확인 포인트]
- 기대 결과: 합성 장면에서 클러스터 3개, 각 중심이 `truth`의 `center`와 가깝고 크기가 `size`와 유사
- 흔한 실수
  - `stat(objects, t0)`를 DBSCAN 뒤에도 같은 클라우드로 기록 → 점 수 변화 없음(시간만 의미)
  - 테이블 면에 붙은 물체 밑면 점이 평면 inlier로 빠져 높이가 약간 작게 측정
  - `labels.max()`가 −1이면 루프 미실행 → 물체 0개, 파라미터 재점검 필요
- 점검 질문
  - `n_noise`를 3000으로 늘리면 어느 단계가 먼저 무너지는가?
  - `eps`를 0.01로 줄이면 클러스터 개수는 어떻게 변하는가?
  - 정답 대비 중심 오차를 자동 계산하는 매칭 함수는 어떻게 짤 것인가?
