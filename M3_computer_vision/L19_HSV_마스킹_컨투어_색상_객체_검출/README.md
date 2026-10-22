# [19강. [실습] HSV 마스킹·컨투어 색상 객체 검출]
- 모듈: ③ 컴퓨터 비전 + 카메라 모델
- 한 줄 요약: 16강 전처리를 함수로 묶고, 컨투어의 면적·원형도로 물체를 골라 중심을 구한 뒤 EMA로 떨림을 줄이는 실시간 색상 검출기를 만드는 실습

## [핵심 개념]
- **처리 파이프라인**
  - 가우시안 블러 → HSV → `inRange` → 열림 → 닫힘 → 컨투어 → 면적·원형도 필터 → 모멘트 중심
- **빨강의 H 감김(wrap-around)**
  - OpenCV H는 $0\sim179$의 원형 축 → 빨강은 0 근처와 179 근처 두 조각
  - 두 마스크를 비트 OR(`|=`)로 합침
- **컨투어**
  - `RETR_EXTERNAL`: 가장 바깥 윤곽만(구멍 내부 윤곽 무시)
  - `CHAIN_APPROX_SIMPLE`: 직선 구간의 중간 점 생략 → 메모리 절약
- **형상 필터**
  - 면적 필터: 작은 점 노이즈 제거
  - 원형도 $C=\frac{4\pi A}{P^2}$: 완전한 원 1, 길쭉하거나 울퉁불퉁할수록 작아짐
- **모멘트 중심**
  - $c_x=\frac{m_{10}}{m_{00}},\;c_y=\frac{m_{01}}{m_{00}}$ ($m_{00}$ = 면적)
  - 바운딩 박스 중심보다 형상 전체를 반영해 안정적
- **EMA로 시간 축 안정화**
  - $\hat c_k=\alpha c_k+(1-\alpha)\hat c_{k-1}$, 코드는 $\alpha=0.3$
  - $\alpha$가 작을수록 부드럽지만 지연 증가(6강 ADC EMA와 같은 트레이드오프)
- **성능 측정**: N 프레임당 경과 시간으로 FPS 계산 → 처리율이 카메라 프레임률을 따라가는지 확인

## [파일별 내용]
- `01_color_detector` — 원본 `src/color_detector.py`의 `make_mask(frame_bgr, lo, hi, lo2=None, hi2=None)`
  - 입력: BGR 프레임, HSV 하한·상한(빨강이면 두 번째 범위 `lo2`/`hi2`까지)
  - 출력: 열림·닫힘으로 정리된 0/255 이진 마스크
  - 5×5 블러, 5×5 타원 커널 고정 → 해상도가 크게 다르면 조정 대상
- `02_컨투어_덩어리를_찾고_재기` — `detect(mask, min_area=300)`
  - `min_area` 미만, 원형도 0.6 미만 컨투어 제외 → 남은 것 중 **최대 면적** 하나 선택
  - 반환: `{"center": (cx, cy), "bbox": (x, y, w, h), "area": ...}` 또는 `None`
  - `peri * peri + 1e-9`: 0 나눗셈 방지
  - 같은 파일(`color_detector.py`)의 연속 부분이라 `cv2`, `np` import는 01에 있음
- `03_시간_축_안정화_검출값_떨림_잡기` — `self.cx = 0.3 * cx + 0.7 * self.cx` 한 줄
  - 클래스 메서드 내부 발췌, `self.cx` 초기화(첫 검출값으로 시작 등)와 `cy` 처리는 생략됨
- `04_run_detector` — 원본 `scripts/run_detector.py`, 웹캠 통합 루프
  - `ColorDetector(config["red"])`: `make_mask` + `detect` + EMA를 묶은 클래스(정의는 발췌에 없음)
  - `det.step(frame)` 결과의 `r["cx"]`, `r["cy"]`, `r["bbox"]`로 중심 원·박스 그림
  - 30 프레임마다 FPS 출력, ESC(키코드 27)로 종료
  - 빠진 맥락: `import time, cv2`, `config` 로드(색 범위 설정 파일), 종료 후 `cap.release()`·`cv2.destroyAllWindows()`
  - 주의: `detect`는 `"center"` 키를 반환하지만 `step`은 `"cx"`/`"cy"`를 반환 → 클래스가 EMA 후 키를 바꿔 담는 구조로 추정

## [선수 지식·연결]
- 16강: HSV, 블러, `inRange`, 모폴로지 각각의 의미
- 6강: ADC 값에 적용한 EMA 필터와 지연 트레이드오프
- 21강: `ColorDetector`를 수정 없이 ROS 2 노드(`color_detector_node`)에 재사용
- 22강 경로 B: 검출한 원의 픽셀 반지름으로 거리 추정

## [실행 전 준비]
- `pip install opencv-python numpy`
- USB 웹캠(`cv2.VideoCapture(0)`)과 GUI 창 표시가 가능한 환경
- 단색(빨간) 공 같은 둥근 물체
- `ColorDetector` 클래스와 색 범위 설정을 직접 작성해 01·02·03을 조립해야 실행 가능

## [확인 포인트]
- 기대 결과: 공 위에 초록 점·박스가 따라다니고, 콘솔에 FPS가 주기적으로 출력
- 흔한 실수
  - 빨강을 범위 하나로만 잡아 조명에 따라 검출이 끊김
  - `min_area`·원형도 임계가 너무 엄격해 멀리 있는 공을 놓침
  - `cv2.rectangle`에 `float` 좌표 전달 → 오류(정수 변환 필요)
- 점검 질문
  - 원형도 0.6은 정사각형($C=\pi/4\approx0.785$)을 통과시키는가?
  - EMA 계수 0.3을 0.1로 바꾸면 빠르게 움직이는 공에서 무엇이 보이는가?
  - FPS가 카메라 프레임률보다 낮다면 어느 단계부터 줄여야 하는가?
