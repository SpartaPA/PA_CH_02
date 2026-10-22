# [31강. [실습] RGBD 깊이 취득·포인트클라우드 변환]
- 모듈: ④ 2D/3D 공간 인지 및 비전 AI
- 한 줄 요약: RealSense에서 컬러에 정렬된 깊이를 미터 단위로 받아 전 픽셀을 벡터화 역투영해 Point Cloud를 만들고, YOLO 검출 박스 × 깊이 × 클러스터링을 합쳐 물체의 3D 위치 획득

## [핵심 개념]
- RGBD 카메라: 컬러 이미지 + 픽셀별 깊이 $Z$(uint16 원값 × `depth_scale` = m)
  - 깊이 0 = 측정 실패(무효) 픽셀
- 정렬(align): 깊이·컬러 센서는 위치·$K$가 다름 → 깊이를 컬러 카메라 시점으로 재투영해야 같은 $(u,v)$가 같은 점을 가리킴
  - 정렬 후에는 컬러 내부파라미터 $K$로 역투영
- 역투영: $X=\frac{(u-c_x)Z}{f_x},\;Y=\frac{(v-c_y)Z}{f_y},\;Z=Z$
  - 23강 `backproject`의 카메라 좌표 부분을 모든 픽셀에 동시 적용
- 벡터화: `np.meshgrid`로 픽셀 격자 생성 → 불리언 마스크로 유효 픽셀만 선택 → 파이썬 루프 없이 한 번에 계산
- 유효 범위 필터 `z_min < Z < z_max`: 센서 최소 거리 이하·먼 거리 노이즈 제거
- ROI 크롭 시 내부파라미터 이동: 잘라낸 영역의 픽셀 $(u',v')=(u-u_0,\,v-v_0)$ → $c_x'=c_x-u_0,\;c_y'=c_y-v_0$
- 검출 × 깊이 × 클라우드: 2D 박스로 탐색 범위를 좁히고, 박스 안 클라우드에서 가장 큰 덩어리를 물체로 선택 → 배경 깊이 섞임 방지

## [파일별 내용]
- `01_rgbd_source.ipynb` — 원본 `src/rgbd_source.py`, `RealSenseSource(w=640, h=480, fps=30)`
  - 컬러 `bgr8`, 깊이 `z16` 스트림 활성화
  - `rs.align(rs.stream.color)`: 깊이를 컬러 기준으로 정렬
  - 컬러 스트림 intrinsics에서 `self.K` 구성(`fx`, `fy`, `ppx`, `ppy`)
  - `read()`: 정렬된 프레임 쌍 → `color`(H,W,3) uint8, `depth`(H,W) float [m]
- `02_depth_to_cloud.ipynb` — 원본 `src/depth_to_cloud.py`, `depth_to_cloud(depth, K, color=None, z_min=0.15, z_max=3.0)`
  - 반환: `xyz`(N,3) 카메라 좌표(OpenCV 규약), `rgb`(N,3) 0~1
  - `color[valid][:, ::-1]`: BGR → RGB 변환(Open3D 색 순서)
  - 빠진 맥락: `import numpy as np`
- `03_합류_검출_깊이_클라우드.ipynb` — 검출 박스마다 ROI 깊이·컬러 크롭 → `K_shifted`로 주점 이동 → `depth_to_cloud` → `to_o3d` → `segment_objects`(30강)
  - 가장 큰 후보의 중심 = 물체 3D 위치, 크기 = 실측 치수
  - `yolo`, `box_of`, `K_shifted`, `to_o3d`, `src`는 정의 없음(29·30강 코드와 헬퍼 결합)
  - ROI에는 테이블 면이 적을 수 있어 평면 제거 단계는 선택 사항

## [선수 지식·연결]
- 23강: 역투영 식, 카메라 좌표 규약
- 27강: 깊이 센서 원리와 정렬(이 폴더 묶음에는 27강 코드 폴더 없음)
- 29강: YOLO 검출 결과(박스) 제공, 평면 가정 3D 승격과 비교
- 30강: `segment_objects`로 ROI 클라우드 정리
- ⑥ 모듈: 깊이·클라우드 → nvblox 3D 재구성·costmap

## [실행 전 준비]
- Intel RealSense 카메라 + `pyrealsense2`(librealsense), USB 3 연결 권장
- `numpy`, `open3d`, `ultralytics`
- 카메라 없을 때: 저장된 컬러·깊이 이미지와 $K$로 `depth_to_cloud`만 시험 가능

## [확인 포인트]
- 기대 결과: 640×480 프레임에서 최대 약 30만 점 클라우드, 시각화 시 장면 형태가 왜곡 없이 재현, 물체 3D 중심이 실측 위치와 근접
- 흔한 실수
  - 정렬 없이 깊이를 컬러 픽셀로 인덱싱 → 물체 가장자리에서 배경 깊이 혼입
  - `depth_scale` 미적용으로 mm 원값을 m로 해석
  - ROI 크롭 후 원래 $K$ 그대로 사용 → 클라우드가 옆으로 밀림
  - `meshgrid`에서 `u`(열)·`v`(행) 순서 혼동
- 점검 질문
  - 박스 안 깊이의 중앙값 하나만 쓰는 방식과 클러스터링 방식의 차이는?
  - 결과 `xyz`를 로봇 `base_link` 좌표로 옮기려면 무엇이 더 필요한가?
  - 반사·투명 물체에서 깊이 0 픽셀이 많을 때 결과는 어떻게 되는가?
