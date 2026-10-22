# [25강. YOLO 계열 객체 검출 파이프라인]
- 모듈: ④ 2D/3D 공간 인지 및 비전 AI
- 한 줄 요약: 단일 단계 검출기 YOLO의 출력 구조(박스·클래스·신뢰도)와 NMS를 이해하고, Ultralytics API로 다섯 줄 추론 구현

## [핵심 개념]
- 객체 검출 = 위치(바운딩 박스) + 종류(클래스) + 신뢰도(score)
- 단일 단계(one-stage) 검출기
  - 한 번의 순전파로 격자/앵커 위치마다 박스·클래스 확률 동시 예측
  - 2단계(후보 영역 → 분류) 방식보다 빠름 → 실시간 로봇 인식에 적합
- 신뢰도 임계값 `conf`: 낮은 점수 박스 제거 → 높이면 정밀도↑ 재현율↓
- NMS(Non-Maximum Suppression)
  - 같은 물체에 겹쳐 나온 박스 중 점수 최고만 남김
  - 겹침 척도 IoU: $\text{IoU}=\frac{|A\cap B|}{|A\cup B|}$, 임계값 `iou` 초과 시 낮은 점수 박스 제거
- 박스 표기: `xyxy`=$(x_1,y_1,x_2,y_2)$ 좌상단·우하단 픽셀, `xywh`=중심·크기
- 모델 크기 n/s/m/l/x: 파라미터 수·정확도·지연의 트레이드오프
- 사전학습 가중치(`yolov8n.pt`)는 COCO 80 클래스 기준 → 다른 대상은 파인튜닝 필요

## [파일별 내용]
- `01_Ultralytics로_추론_다섯_줄.ipynb` — 교안 "Ultralytics로 추론" 코드 발췌
  - `YOLO("yolov8n.pt")`: 가장 작은 nano 모델 로드(없으면 자동 다운로드)
  - `model(frame, conf=0.5)`: `frame`은 16강의 `(H,W,3)` BGR uint8 ndarray
  - `results[0].boxes`: 첫 이미지의 검출 목록
    - `b.xyxy[0]`: 박스 좌표 텐서, `int(b.cls)`: 클래스 번호, `float(b.conf)`: 신뢰도
    - 클래스 이름은 `model.names[cls]`
  - 빠진 맥락: `frame` 획득 코드(`cv2.imread`/`VideoCapture`), 결과 그리기·출력 코드 없음

## [선수 지식·연결]
- 16강: 이미지 = NumPy 배열(BGR) → YOLO 입력 그대로 사용
- 29강: 이 추론을 ROS 2 노드로 감싸 `vision_msgs/Detection2DArray` 발행, `conf`·`iou`를 ROS 파라미터화
- 31강: 검출 박스를 깊이 ROI로 써서 물체 3D 위치 획득
- ⑨ 모듈: ONNX/TensorRT로 같은 모델 가속

## [실행 전 준비]
- `pip install ultralytics`(PyTorch 포함), `opencv-python`
- GPU 있으면 CUDA 버전 PyTorch, 없으면 CPU로도 nano 모델 동작
- 첫 실행 시 가중치 다운로드용 네트워크 필요

## [확인 포인트]
- 기대 결과: 사람·컵 등 COCO 물체에 대해 박스 좌표·클래스·신뢰도 출력
- 흔한 실수
  - RGB 이미지를 넣었다고 착각하거나 PIL/ndarray 색 순서 혼동
  - `results`가 리스트임을 잊고 `results.boxes` 접근
  - 텐서를 그대로 출력/연산 → `float()`·`.cpu().numpy()` 변환 필요
- 점검 질문
  - `conf`를 0.25 → 0.7로 올리면 오검출·미검출이 각각 어떻게 변하는가?
  - NMS의 `iou` 임계값을 너무 낮추면 붙어 있는 두 물체에 무슨 일이 생기는가?
  - n과 s 모델의 지연·정확도 차이를 직접 재 보면?
