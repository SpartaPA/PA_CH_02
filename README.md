# PA_CH_02 — [CH 2] Physical AI 실행 코드 모음

Physical AI Robotics Level 2 교안([CH 2] Physical AI, teamsparta.notion.site)에서 **프로그래밍 언어로 실행할 수 있는 부분(코드 블록)만** 모아 모듈·강의별로 정리한 저장소입니다. 이 문서는 각 코드가 **어떤 이론 위에서 돌아가는지**를 설명합니다.

- 원본: <https://teamsparta.notion.site/CH-2-Physical-AI-3c02dc3ef5148093ac7ff3ccf54a4f81>
- 수집 범위: 공개된 하위 페이지 73개(모듈 8개 + 강의 64개), 토글 속 "심화" 블록까지 전부 → **코드 블록 128개** (Python 74 · C 32 · Bash 18 · YAML 1 · 텍스트 3)
- 모듈 ⑤·⑩(팀 프로젝트)은 공개 하위 페이지가 없어 포함되지 않았습니다. 코드 블록이 없는 이론 강의(2·9~12·27·37~40·46·48·49·56~58·64~66강)는 폴더가 없습니다.

---

## 1. 폴더 구조

```
PA_CH_02/
├── README.md                 ← 이 문서 (실행의 이론적 바탕)
├── reference.md              ← 핵심 참고 서적
├── requirements.txt          ← Python 의존성
├── M1_embedded_control/      ① 임베디드 제어 기초        (1~8강)
├── M2_kinematics_dynamics/   ② 로봇 기구학 및 동역학      (9~15강)
│   └── runnable/             ★ 13~15강 코드를 묶은 실행·테스트 패키지
├── M3_computer_vision/       ③ 컴퓨터 비전 + 카메라 모델   (16~22강)
├── M4_3d_perception/         ④ 2D/3D 공간 인지 및 비전 AI (23~31강)
├── M6_slam_nav2/             ⑥ SLAM 및 Nav2 자율주행      (37~45강)
├── M7_imitation_learning/    ⑦ 모방학습 및 정책 최적화     (46~54강)
├── M8_sim2real/              ⑧ Sim2Real 및 물리 시뮬레이션 (55~62강)
└── M9_edge_deployment/       ⑨ 에지 컴퓨팅 및 실시간 배포  (63~69강)
```

강의 폴더 안의 파일 이름은 `순번_원본파일명` 또는 `순번_교안의절제목` 형식입니다. 모든 파일 첫머리에 **출처 강의 · 절 · (있으면) 교안이 지정한 원본 경로**(예: `src/fk_chain.py`)가 주석으로 달려 있습니다. 강의 폴더 안의 코드는 교안 원문 그대로이며, 교안이 "핵심부"만 보여 준 발췌도 많습니다.

### 실행 형태별 구분

| 구분 | 해당 파일 | 실행 방법 |
|---|---|---|
| **바로 실행·테스트** | `M2_kinematics_dynamics/runnable/`, `L01/01_*.py` | 아래 2절 |
| Python 발췌(라이브러리 필요) | M3·M4·M7·M8·M9의 `.py` | OpenCV / Open3D / PyTorch / ONNX 환경에서 앞뒤 맥락과 함께 조립 |
| ROS 2 노드·명령 | `*_node.py`, `*.sh`, `waypoints.yaml` | ROS 2 Lyrical + Isaac ROS 5.0 (PC), Isaac Sim |
| MCU 펌웨어 (C) | M1의 `.c` | STM32CubeIDE의 HAL 프로젝트 (`USER CODE` 구역에 삽입), OpenCR |
| 의사코드 | `*_의사코드.txt` 3개 | 교안 자체가 구조 설명용 의사코드라 실행용이 아님 |

---

## 2. 바로 실행해 보기

```bash
cd PA_CH_02
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy matplotlib pytest

# 모듈 ② : 13~15강 코드 묶음 — 테스트 14개
cd M2_kinematics_dynamics/runnable
python -m pytest -q                       # 14 passed
python demos/demo_fk_workspace.py         # 13강: FK·작업공간 → demos/out/fk_workspace.png
python demos/demo_singularity.py          # 14강: pinv vs DLS 특이점 통과 → demos/out/singularity.png
python demos/demo_tracking.py             # 15강: 계단/Quintic × PID/PID+중력보상 → demos/out/tracking.png
```

이 저장소를 만들면서 실제로 돌려 본 결과:

| 실험 | 결과 |
|---|---|
| `pytest` | 14 passed (FK 기지 자세 6, Jacobian 해석해=수치미분 3, 특이점 1, 동역학 4) |
| 작업 공간 | 손끝 도달 반경 0.100 ~ 0.500 m (이론값 \|L1−L2\| ~ L1+L2 와 일치) |
| 특이점 통과 | 순정 pinv 최대 관절속도 **236.5 rad/s** (폭주) vs DLS **0.39 rad/s** |
| 궤적 추종 RMS | 계단+PID 0.165 · 계단+PID+g 0.158 · Quintic+PID 0.072 · **Quintic+PID+g 0.0099 rad** |

`L01/01_Python으로_눈으로_확인하기.py`는 그림만 그리므로 끝에 `plt.show()`를 붙이거나 노트북에서 실행하세요.

---

## 3. 실습 환경 (교안 기준)

- PC: Ubuntu 24.04 + NVIDIA Isaac ROS 5.0 + ROS 2 Lyrical
- Raspberry Pi 4B: Ubuntu Server 26.04 arm64 + ROS 2 Lyrical. OpenCR의 빌드·업로드·시리얼 확인은 Pi에 SSH로 접속해 수행
- 하드웨어(프로젝트 1): RealSense D435i · Dynamixel · OpenCR 기반 1축 비전 추적. 이동로봇·로봇팔은 Isaac Sim 가상 환경
- Python 실습(②③④⑦): venv + JupyterLab. 노트북은 탐색과 설명용, `.py` 모듈은 재사용할 도구

---

## 4. 실행의 바탕 — 모듈별 이론

### ① 임베디드 제어 기초 (1~8강) — `M1_embedded_control/`

**플랜트 응답(1강).** 1차계 $G(s)=\frac{1}{\tau s+1}$의 계단 응답은 $y=1-e^{-t/\tau}$이고, 2차계 $G(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$는 감쇠비 $\zeta<1$에서 감쇠 진동 $\omega_d=\omega_n\sqrt{1-\zeta^2}$로 오버슈트를 만듭니다. `L01`은 이 두 식을 그대로 그립니다. 극점의 실수부가 정착시간을, 허수부가 진동을 결정합니다(2강).

**PID와 이산화(3·7강).** 연속 PID $u=K_pe+K_i\int e\,dt+K_d\dot e$를 MCU에서 주기 $dt$로 돌리려면 적분은 누적합, 미분은 차분으로 바꿉니다. 출력이 포화될 때 적분이 계속 쌓이는 **windup**을 막으려고 포화 중에는 적분을 멈춥니다(clamping anti-windup). `L03`의 C 코드와 `L07/02_PID_모듈_구현.c`가 이를 구현하고, `L07/03_ISR에서_조립.c`는 타이머 인터럽트로 제어 주기를 고정합니다. ISR과 메인 루프가 공유하는 변수에 `volatile`을 붙이는 이유도 여기서 다룹니다.

**MCU 주변장치(4~6강).** Cortex-M에서 모든 주변장치는 메모리 주소이고(`L04`: GPIO ODR 비트 쓰기), PWM 듀티비는 모터 평균 전압에, 주파수는 서보(50 Hz)와 DC 모터(약 21 kHz, 가청 대역 밖)에서 다르게 쓰입니다(`L05`). 센서 쪽에서는 ADC 원값에 지수이동평균(EMA) $y_k=\alpha x_k+(1-\alpha)y_{k-1}$을 걸어 떨림을 줄이고, 쿼드러처 엔코더 카운트 차분 $\Delta N$에서 $\text{RPM}=\frac{\Delta N}{\text{CPR}}\cdot\frac{60}{\Delta t}$로 속도를 구합니다(`L06`).

**micro-ROS(8강).** MCU를 ROS 2 그래프의 노드로 만들어 시리얼로 Agent에 붙고, 50 Hz로 상태를 publish하며 목표 속도를 subscribe합니다. 작은 링크에서는 QoS(best-effort와 reliable)를 신중히 고릅니다.

### ② 로봇 기구학 및 동역학 (9~15강) — `M2_kinematics_dynamics/`

**순기구학(9·13강).** 링크마다 D-H 파라미터 한 행 $(\theta,d,a,\alpha)$가 동차변환 하나가 됩니다.
$$T_{i-1}^{\,i}=R_z(\theta)\,T_z(d)\,T_x(a)\,R_x(\alpha),\qquad T_0^{\,n}=\prod_i T_{i-1}^{\,i}$$
`transforms.py`의 `dh_transform`이 이 곱이고, `fk_chain.py`의 `PlanarArm`이 사슬을 누적합니다. 평면 2링크의 손끝은 $x=L_1c_1+L_2c_{12},\;y=L_1s_1+L_2s_{12}$이며 `test_fk.py`가 이를 기지 자세로 고정합니다.

**Jacobian과 특이점(11·14강).** 관절 속도와 손끝 속도는 $\dot x=J(\theta)\dot\theta$로 이어집니다. 평면 팔의 $j$번째 열은 $j$번째 관절 뒤쪽 링크 벡터 합을 90° 돌린 것입니다(`jacobian_planar`). 같은 값을 중앙차분 $\frac{f(\theta+\epsilon)-f(\theta-\epsilon)}{2\epsilon}$으로도 구해 서로 맞는지 확인합니다. 역방향 $\dot\theta=J^{+}\dot x$는 $J$의 최소 특이값 $\sigma_{\min}\to0$(팔이 다 펴짐)에서 폭주합니다. 특이점 지표로는 조작성 $w=\sqrt{\det JJ^\top}$, $\sigma_{\min}$, 조건수를 쓰고, 처방은 **Damped Least Squares** $\dot\theta=J^\top(JJ^\top+\lambda^2I)^{-1}\dot x$입니다.

**역기구학(10강).** Newton–Raphson 반복 $\theta\leftarrow\theta+J^{+}(x^\*-f(\theta))$은 위 Jacobian 코드를 그대로 재사용합니다(10강 본문은 이론 위주라 코드 블록이 없음).

**동역학과 중력 보상(12·15강).** 로봇팔 관절은 자세에 따라 성질이 바뀌는 플랜트입니다.
$$M(\theta)\ddot\theta+C(\theta,\dot\theta)\dot\theta+g(\theta)=\tau$$
$M$은 대칭·양의 정부호이고 $\cos\theta_2$ 항 때문에 팔꿈치를 펼수록 커집니다. 그래서 튜닝은 관성이 가장 큰 자세에서 합니다. 중력 보상 $\tau=\text{PID}(e)+\hat g(\theta)$는 이미 아는 힘을 미리 내주고, 피드백에는 모델이 못 맞춘 나머지만 맡깁니다. 15강의 **Quintic 궤적**은 위치·속도·가속도 경계조건 6개를 만족하는 5차 다항식입니다.
$$\theta(t)=\theta_0+\Delta\left(10\tfrac{t^3}{T^3}-15\tfrac{t^4}{T^4}+6\tfrac{t^5}{T^5}\right)$$
시작과 끝에서 가속도가 0이라 계단 입력보다 토크 충격이 작습니다. 위 2절의 RMS 결과가 이 두 가지 효과를 수치로 보여 줍니다.

### ③ 컴퓨터 비전 + 카메라 모델 (16~22강) — `M3_computer_vision/`

**이미지 = 배열(16·19강).** OpenCV 이미지는 `(H,W,3)` uint8 BGR NumPy 배열입니다. HSV는 색상(H)과 밝기(V)를 분리하므로 조명이 바뀌어도 색 마스크가 잘 유지됩니다. 처리 순서는 가우시안 블러 → `inRange` 마스크 → 열림/닫힘 모폴로지 → 컨투어 → 면적·원형도 필터 → 모멘트 중심입니다. 검출값 떨림은 EMA로 줄이는데, 그만큼 지연이 생깁니다.

**핀홀 모델과 왜곡(17·20강).**
$$s\begin{bmatrix}u\\v\\1\end{bmatrix}=K\,[R\,|\,t]\begin{bmatrix}X\\Y\\Z\\1\end{bmatrix},\qquad K=\begin{bmatrix}f_x&0&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}$$
렌즈는 방사 왜곡 $(k_1,k_2,k_3)$과 접선 왜곡 $(p_1,p_2)$을 더합니다. Zhang의 체커보드 캘리브레이션(`calibrate.py`)은 여러 장의 평면 대응점으로 $K$와 왜곡계수를 추정하고, **재투영 오차 RMS**로 결과의 품질을 판정합니다.

**PnP와 단안 거리(18·22강).** 알려진 3D 점과 2D 투영 사이의 대응에서 $[R|t]$를 구하는 문제가 PnP입니다(`cv2.solvePnP`). 단안 카메라는 크기를 모르면 거리를 정할 수 없습니다. 그래서 크기를 아는 물체를 쓰면 $Z=\frac{f\cdot D}{d_{px}}$로 깊이를 얻습니다(22강 경로 B). ArUco 마커는 대응점 문제를 미리 풀어 둔 실전 PnP 도구입니다(경로 A).

**ROS 2 연동(21·22강).** `cv_bridge`가 `sensor_msgs/Image`와 OpenCV 배열을 서로 바꿔 주고, `CameraInfo`가 $K$와 왜곡계수를 함께 보냅니다. 결과는 `PoseStamped`와 RViz2 Marker로 보이고, rosbag 재생으로 회귀 시험을 합니다.

### ④ 2D/3D 공간 인지 및 비전 AI (23~31강) — `M4_3d_perception/`

**좌표 사슬(23강).** World → Camera(외부파라미터 $R,t$) → 정규화 이미지 평면 → Pixel(내부파라미터 $K$). `project()`와 역방향 `backproject()`로 한 바퀴 돌아 원래 점으로 돌아오는지 검증합니다. OpenCV 카메라 좌표(z 전방)와 ROS 좌표(x 전방)의 규약 차이에 주의합니다.

**PnP 심화(24·28강).** P3P는 최소 3점으로 해를 최대 4개까지 냅니다. EPnP는 n개 점을 가상 제어점 4개의 가중합으로 표현해 $O(n)$에 풉니다. 대응 중 이상치가 섞이면 **RANSAC**으로 최소 표본 가설을 세우고 inlier 합의로 고릅니다(`solvePnPRansac`). `pnp_bench.py`는 정답을 아는 합성 데이터로 노이즈·점 개수·이상치 비율별 오차를 측정합니다.

**YOLO(25·29강).** 단일 단계 검출기로, 한 번의 순전파로 박스·클래스·신뢰도를 내고 NMS로 겹치는 박스를 정리합니다. ROS 노드는 표준 메시지 `vision_msgs/Detection2DArray`로 결과를 발행합니다. 입력 해상도와 처리율(Hz) 사이의 동작점을 측정해 고르고, 박스 밑변 중심을 바닥 평면과 교차시켜 3D 위치로 올립니다.

**Point Cloud(26·30강).** 점 집합은 순서가 없어 격자 연산을 바로 쓸 수 없습니다. 처리 순서는 Voxel 다운샘플(점 수 감소) → SOR(이웃 평균거리가 $\mu+k\sigma$를 넘는 점 제거) → RANSAC 평면 $ax+by+cz+d=0$ 추출(테이블·바닥) → DBSCAN 클러스터링(개체 분리)입니다. `synth_scene.py`가 정답 라벨이 있는 장면을 만들어 단계별로 계량합니다.

**RGBD 역투영(27·31강).** 깊이 $Z$와 픽셀 $(u,v)$에서 $X=\frac{(u-c_x)Z}{f_x},\;Y=\frac{(v-c_y)Z}{f_y}$입니다. `depth_to_cloud.py`는 이를 30만 픽셀에 벡터화해 한 번에 계산합니다. 깊이와 컬러의 정렬(align)이 먼저 되어 있어야 하고, 검출 박스 × 깊이 × 클라우드를 합쳐 물체의 3D 위치를 얻습니다.

### ⑥ SLAM 및 Nav2 자율주행 (37~45강) — `M6_slam_nav2/`

**SLAM과 상태 추정(37~39강).** 사후 확률은 $p(x_t|z_{1:t},u_{1:t})\propto p(z_t|x_t)\int p(x_t|x_{t-1},u_t)\,p(x_{t-1}|\cdot)\,dx_{t-1}$로, 예측(모션 모델)과 갱신(관측 우도)의 곱입니다. Kalman/EKF는 이 분포를 가우시안으로, AMCL(Particle Filter)은 표본으로 표현합니다. 루프 폐합은 다시 찾은 장소의 제약을 포즈 그래프에 넣어 누적 드리프트를 분산시킵니다. 41·42강의 bash 스크립트는 NVIDIA **cuVSLAM**(시각-관성 SLAM)과 **nvblox**(3D 재구성 → costmap) 지도를 만들고, 저장·로드한 뒤 `localize_in_map`으로 재위치를 추정하고 TF 사슬(map→odom→base_link)을 확인합니다.

**Nav2(40·43~45강).** Behavior Tree가 전역 플래너(경로)와 로컬 컨트롤러(속도 명령)를 조율하고, costmap 레이어(static/obstacle/inflation)가 장애물을 비용장으로 바꿉니다. `patrol_node.py`는 `nav2_simple_commander`로 `NavigateToPose`/`followWaypoints` 액션을 호출하고, 경유지는 `waypoints.yaml`로 분리합니다. 44~45강은 성공률, 소요시간, 재계획 횟수를 반복 측정하는 벤치마크(`bench_runner.py`)와 회귀 게이트로 튜닝 결과를 채택할지 판정합니다.

### ⑦ 로봇 모방학습 및 정책 최적화 (46~54강) — `M7_imitation_learning/`

**Behavior Cloning(47·51강).** 시연 $(o,a)$ 쌍에 대한 지도학습 $\min_\pi\mathbb E\,\|\pi(o)-a\|^2$입니다. `train_bc.py`는 아키텍처(MLP/CNN/Transformer)만 갈아 끼우는 공용 학습기입니다. 50강 데이터 정합(다주기 스트림을 타임스탬프로 보간해 짝짓기, 노이즈 필터, HDF5 저장)이 성능의 전제입니다.

**공변량 이동과 DAgger(49·54강).** BC는 자기 실수로 처음 보는 상태에 들어가면 오차가 누적됩니다(대략 $O(T^2)$). DAgger는 학습된 정책으로 롤아웃한 상태에 전문가 라벨을 붙여 데이터셋에 합쳐서 이 문제를 $O(T)$로 줄입니다. HG-DAgger는 사람이 개입한 구간만 라벨로 씁니다.

**Diffusion Policy(48·52강).** 행동 분포가 다봉일 때(장애물을 왼쪽/오른쪽으로 돌기) MSE 회귀는 두 답의 평균, 즉 충돌 경로를 냅니다. 확산 모델은 순방향 $a_k=\sqrt{\bar\alpha_k}a_0+\sqrt{1-\bar\alpha_k}\epsilon$에서 노이즈 $\epsilon$을 예측하도록 $\|\epsilon-\epsilon_\theta(a_k,k,o)\|^2$로 학습하고, 역과정으로 행동 **시퀀스**를 샘플링합니다. 실행은 receding horizon(일부만 실행 후 재계획)으로 합니다.

**평가(53강).** 성공률, 완료 시간, jerk 기반 Smoothness를 시드 여러 개로 측정하고 신뢰구간과 함께 보고합니다.

### ⑧ Sim2Real 및 가상 물리 시뮬레이션 (55~62강) — `M8_sim2real/`

**병렬 시뮬레이션(55·59강).** Isaac Lab은 USD 장면을 GPU에서 수천 개 병렬 환경으로 돌리고, 태스크는 `reset(env_ids)`/`step(actions)` 인터페이스로 정의합니다. 관측에는 실물에서도 구할 수 있는 값만 넣습니다.

**도메인 랜덤화(56·60강).** 텍스처, 조명, 질량, 마찰을 분포 $\xi\sim p(\xi)$에서 뽑아 학습합니다. 목표는 $\max_\pi\mathbb E_{\xi}[R(\pi;\xi)]$이고, 현실을 그 분포의 한 표본으로 만드는 것입니다. **ADR**은 성공률이 임계를 넘으면 랜덤화 폭을 넓히는 커리큘럼입니다(`adr.py`).

**Gap 분석과 보정(57·58·61·62강).** 실물에서 기록한 궤적을 시뮬에서 재생해 오차를 목적함수로 두고 물리 파라미터를 추정합니다(**System ID**, `sysid.py`, $\min_\phi\sum\|x^{real}_t-x^{sim}_t(\phi)\|^2$). 그다음 소량의 실데이터로 fine-tuning합니다. 배포 단계에서는 정책을 추론 전용으로 내보내 ROS 노드에서 실행합니다.

### ⑨ 에지 컴퓨팅 및 실시간 배포 (63~69강) — `M9_edge_deployment/`

**ONNX/ONNXRuntime(63강).** `torch.onnx.export`로 프레임워크 독립 그래프를 만들면, ORT가 상수 접기와 연산자 융합(Conv+BN+ReLU 등) 같은 그래프 최적화를 하고, Execution Provider(CPU/CUDA/TensorRT)로 하드웨어를 고릅니다.

**TensorRT와 양자화(64·67강).** FP16은 대개 정확도 손실이 거의 없이 처리량을 올립니다. INT8은 $q=\text{round}(x/s)$ 스케일 $s$를 대표 입력의 활성값 분포로 정하는 **캘리브레이션**이 필요합니다. `trtexec`와 Python API 두 경로로 엔진을 만들고, 변환 전후 출력 정합(오차 허용치)을 확인합니다.

**실시간성(65·66·68·69강).** 평균 지연보다 **꼬리 지연(P99)**과 deadline miss가 제어 안정성을 결정합니다. `profiler.py`는 전처리/추론/후처리 구간을 나눠 분포를 기록합니다. 최종 추론 노드는 워밍업, 버퍼 사전 할당, 최신 프레임 슬롯, 미스 정책(버림 → 외삽 → HOLD)을 모두 갖춥니다. Jetson Orin/Thor 배포에서는 전력 모드와 온도 스로틀링까지 측정합니다.

---

## 5. 원문 대비 보강·수정 사항

강의 폴더(`L??_*`)의 파일은 교안 원문 그대로입니다. 아래는 `M2_kinematics_dynamics/runnable/`에서만 손댄 내용입니다.

- `src/arm_dynamics.py`: 교안은 `M()`, `C()`, `gvec()`를 `...`로 생략했습니다. 여기서는 **링크 끝 점질량, 수직 평면 2링크(θ는 수평 기준)** 모델로 채우고 `energy()`를 추가했습니다. `step()`(semi-implicit Euler)은 원문 그대로입니다.
- 교안의 에너지 보존 테스트(오일러, 허용 1e-2)는 초기자세 (0.3, 0.5) rad에서 5초 자유 진동 동안 에너지가 약 25% 빠져 통과하지 못합니다. 원인은 모델이 아니라 적분기입니다(RK4에서는 오차 2×10⁻⁸). 그래서 `step_rk4()`를 추가하고, 테스트는 RK4로 모델을 검증하도록 바꿨습니다.
- 특이점 테스트의 조작성 허용치를 1e-6으로 조정했습니다($\sqrt{\det}$ 연산의 수치 잔차 때문).
- `Arm3D.fk()`가 (x, y, z)를 돌려주도록 재정의했습니다(부모의 `fk`는 평면용 (x, y)).
- 데모 3개는 13~15강 본문의 실험 절차를 실행 가능한 스크립트로 옮긴 것입니다.

---

## 6. 전체 파일 색인

#### M1_embedded_control

| 강의 폴더 | 파일 |
|---|---|
| [L01_제어_개요와_시스템_응답](M1_embedded_control/L01_제어_개요와_시스템_응답/) | `01_Python으로_눈으로_확인하기.py` |
| [L03_PID_제어와_튜닝](M1_embedded_control/L03_PID_제어와_튜닝/) | `01_이산화_MCU_위의_PID.c`<br>`02_대표_대책_anti_windup.c` |
| [L04_MCU와_주변장치](M1_embedded_control/L04_MCU와_주변장치/) | `01_메모리맵_모든_것은_주소다.c` |
| [L05_GPIO_타이머_PWM_액추에이터_구동](M1_embedded_control/L05_GPIO_타이머_PWM_액추에이터_구동/) | `01_빌드_플래시_관찰_사이클.c`<br>`02_폴링_방식.c`<br>`03_인터럽트_방식.c`<br>`04_코드.c`<br>`05_설정과_코드.c` |
| [L06_ADC_엔코더_센서_인터페이스](M1_embedded_control/L06_ADC_엔코더_센서_인터페이스/) | `01_설정과_코드_가변저항_읽기.c`<br>`02_UART_로깅_측정을_눈으로.c`<br>`03_필터_떨리는_값_다듬기.c`<br>`04_STM32_타이머_엔코더_모드.c`<br>`05_속도_계산.c`<br>`06_통합_오늘의_결과물.c` |
| [L07_PID_펌웨어_목표값_추종](M1_embedded_control/L07_PID_펌웨어_목표값_추종/) | `01_공유_변수와_volatile.c`<br>`02_PID_모듈_구현.c`<br>`03_ISR에서_조립.c`<br>`04_위치_제어로_확장.c` |
| [L08_micro_ROS_ROS2_네트워크_연동](M1_embedded_control/L08_micro_ROS_ROS2_네트워크_연동/) | `01_노드_코드.c`<br>`02_Agent_실행과_접속_확인.sh`<br>`03_Agent_실행과_접속_확인.sh`<br>`04_조작과_관찰.sh` |

#### M2_kinematics_dynamics

| 강의 폴더 | 파일 |
|---|---|
| [L13_2_3DOF_FK_동차변환_체인](M2_kinematics_dynamics/L13_2_3DOF_FK_동차변환_체인/) | `01_transforms.py`<br>`02_기본_변환_블록_만들기.py`<br>`03_fk_chain.py`<br>`04_FK_체인_로봇을_데이터로_표현하기.py`<br>`05_test_fk.py`<br>`06_자세_그리기.py`<br>`07_작업_공간_FK를_몬테카를로로.py`<br>`08_3D로_확장.py` |
| [L14_Jacobian_속도_변환_특이점_탐지](M2_kinematics_dynamics/L14_Jacobian_속도_변환_특이점_탐지/) | `01_jacobian.py`<br>`02_수치_미분_Jacobian_검증자.py`<br>`03_test_jacobian.py`<br>`04_속도_변환_정방향과_역방향.py`<br>`05_특이점_탐지_지표를_코드로.py`<br>`06_특이점_통과_실험_폭주를_눈으로.py`<br>`07_특이점_통과_실험_폭주를_눈으로.py` |
| [L15_Quintic_궤적_생성_PID_튜닝](M2_kinematics_dynamics/L15_Quintic_궤적_생성_PID_튜닝/) | `01_trajectory.py`<br>`02_arm_dynamics.py`<br>`03_시뮬레이터_12강_동역학을_코드로.py`<br>`04_추종_실험_계단_vs_Quintic_PID_vs_PID_중력_보상.py` |

#### M3_computer_vision

| 강의 폴더 | 파일 |
|---|---|
| [L16_OpenCV_기초](M3_computer_vision/L16_OpenCV_기초/) | `01_이미지_NumPy_배열.py`<br>`02_이미지_NumPy_배열.py`<br>`03_색공간_왜_HSV인가.py`<br>`04_필터링_노이즈를_눌러야_마스크가_깨끗하다.py`<br>`05_이진화와_모폴로지_마스크_청소.py` |
| [L17_핀홀_카메라_모델과_렌즈_왜곡](M3_computer_vision/L17_핀홀_카메라_모델과_렌즈_왜곡/) | `01_언제_반드시_보정해야_하나.py` |
| [L18_PnP_포즈_추정과_단안_거리_모호성](M3_computer_vision/L18_PnP_포즈_추정과_단안_거리_모호성/) | `01_PnP_문제의_정의.py` |
| [L19_HSV_마스킹_컨투어_색상_객체_검출](M3_computer_vision/L19_HSV_마스킹_컨투어_색상_객체_검출/) | `01_color_detector.py`<br>`02_컨투어_덩어리를_찾고_재기.py`<br>`03_시간_축_안정화_검출값_떨림_잡기.py`<br>`04_run_detector.py` |
| [L20_체커보드_카메라_캘리브레이션](M3_computer_vision/L20_체커보드_카메라_캘리브레이션/) | `01_calibrate.py`<br>`02_코너_검출과_캘리브레이션_실행.py`<br>`03_관문_③_눈_검사_undistort.py`<br>`04_적용_저장_불러오기_즉시_활용.py` |
| [L21_cv_bridge_ROS2_이미지_토픽_연동](M3_computer_vision/L21_cv_bridge_ROS2_이미지_토픽_연동/) | `01_두_가지_표준_메시지.sh`<br>`02_color_detector_node.py`<br>`03_실행과_확인.sh` |
| [L22_검출_포즈추정_비전_파이프라인_통합](M3_computer_vision/L22_검출_포즈추정_비전_파이프라인_통합/) | `01_aruco_pose_node.py`<br>`02_경로_B_색_검출_거리_추정.py`<br>`03_RViz2_시각화_3D로_보는_첫_순간.sh`<br>`04_rosbag_회귀_시험.sh` |

#### M4_3d_perception

| 강의 폴더 | 파일 |
|---|---|
| [L23_카메라_좌표계_변환_심화](M4_3d_perception/L23_카메라_좌표계_변환_심화/) | `01_사슬_왕복_코드로_검증.py` |
| [L24_PnP_심화](M4_3d_perception/L24_PnP_심화/) | `01_이상치의_세계_RANSAC.py` |
| [L25_YOLO_계열_객체_검출_파이프라인](M4_3d_perception/L25_YOLO_계열_객체_검출_파이프라인/) | `01_Ultralytics로_추론_다섯_줄.py` |
| [L26_Point_Cloud_표현_처리](M4_3d_perception/L26_Point_Cloud_표현_처리/) | `01_표현_순서_없는_점들의_집합.py`<br>`02_필터_①_Voxel_다운샘플_점을_줄여야_시작된다.py`<br>`03_필터_②_SOR_통계로_이상치_걷어내기.py`<br>`04_평면_추출_RANSAC의_재등판.py`<br>`05_클러스터링_덩어리를_개체로.py` |
| [L28_cv2_solvePnP_2D_3D_포즈_추정](M4_3d_perception/L28_cv2_solvePnP_2D_3D_포즈_추정/) | `01_pnp_bench.py`<br>`02_실험_3_RANSAC_오염_실험.py`<br>`03_실물_상자_포즈_추정기.py` |
| [L29_YOLO_추론_ROS2_통합](M4_3d_perception/L29_YOLO_추론_ROS2_통합/) | `01_yolo_node.py`<br>`02_실시간성_측정과_동작점_선택.sh`<br>`03_3D_승격_어디에_까지.py` |
| [L30_Point_Cloud_필터링](M4_3d_perception/L30_Point_Cloud_필터링/) | `01_synth_scene.py`<br>`02_segment.py`<br>`03_실데이터_적용과_시각화.py` |
| [L31_RGBD_깊이_취득_포인트클라우드_변환](M4_3d_perception/L31_RGBD_깊이_취득_포인트클라우드_변환/) | `01_rgbd_source.py`<br>`02_depth_to_cloud.py`<br>`03_합류_검출_깊이_클라우드.py` |

#### M6_slam_nav2

| 강의 폴더 | 파일 |
|---|---|
| [L41_cuVSLAM_nvblox_3D_지도_생성_저장_로드](M6_slam_nav2/L41_cuVSLAM_nvblox_3D_지도_생성_저장_로드/) | `01_배선_39강_회로도의_실물화.sh`<br>`02_배선_39강_회로도의_실물화.sh`<br>`03_서로_다른_세_가지_산출물.sh`<br>`04_재로드_확인.sh` |
| [L42_cuVSLAM_지도_재위치_추정_추적_복구](M6_slam_nav2/L42_cuVSLAM_지도_재위치_추정_추적_복구/) | `01_배선_시각_지도_로드와_TF_공급.sh`<br>`02_배선_시각_지도_로드와_TF_공급.sh`<br>`03_실험_A_위치_힌트_오차와_재위치_추정.sh` |
| [L43_Nav2_다중_Waypoint_주행](M6_slam_nav2/L43_Nav2_다중_Waypoint_주행/) | `01_풀스택_기동과_첫_주행.sh`<br>`02_patrol_node.py`<br>`03_waypoints.yaml`<br>`04_두_가지_실행_방식.py`<br>`05_nav_logger.py` |
| [L44_Planner_Costmap_튜닝_동적_장애물_회피](M6_slam_nav2/L44_Planner_Costmap_튜닝_동적_장애물_회피/) | `01_회귀_게이트_채택의_조건.sh` |
| [L45_주행_성공률_소요시간_재계획_측정](M6_slam_nav2/L45_주행_성공률_소요시간_재계획_측정/) | `01_bench_runner.py` |

#### M7_imitation_learning

| 강의 폴더 | 파일 |
|---|---|
| [L47_Behavior_Cloning_정책_학습](M7_imitation_learning/L47_Behavior_Cloning_정책_학습/) | `01_우리의_실습_무대_2링크_도달_과제_51강_예열.py` |
| [L50_시연_데이터_시계열_정합_노이즈_제거](M7_imitation_learning/L50_시연_데이터_시계열_정합_노이즈_제거/) | `01_collector.py`<br>`02_align.py`<br>`03_산출물_HDF5와_품질_리포트.txt` |
| [L51_MLP_CNN_Transformer_BC_정책_학습](M7_imitation_learning/L51_MLP_CNN_Transformer_BC_정책_학습/) | `01_train_bc.py`<br>`02_②_CNN_이미지_관측_의사코드.txt`<br>`03_rollout_eval.py` |
| [L52_Diffusion_Policy_비정형_조작_학습](M7_imitation_learning/L52_Diffusion_Policy_비정형_조작_학습/) | `01_갈림길_데이터셋_저주를_설계하다.sh`<br>`02_①_노이즈_예측_네트워크.py`<br>`03_②_학습_루프_48강_수식_그대로.py`<br>`04_③_샘플링과_리시딩_호라이즌_실행.py` |
| [L53_정책_성능](M7_imitation_learning/L53_정책_성능/) | `01_평가기_정책을_꽂으면_리포트가_나온다.py` |
| [L54_DAgger_HG_DAgger_데이터_효율화](M7_imitation_learning/L54_DAgger_HG_DAgger_데이터_효율화/) | `01_expert.py`<br>`02_dagger.py`<br>`03_hg_dagger.py` |

#### M8_sim2real

| 강의 폴더 | 파일 |
|---|---|
| [L55_Isaac_Sim_Isaac_Lab_태스크_구성](M8_sim2real/L55_Isaac_Sim_Isaac_Lab_태스크_구성/) | `01_병렬성_이_도구의_존재_이유.py` |
| [L59_Isaac_로봇_태스크_센서_환경_구성](M8_sim2real/L59_Isaac_로봇_태스크_센서_환경_구성/) | `01_태스크_구현_명세서의_코드화_의사코드.txt`<br>`02_기준_학습_성립_의_증명.py` |
| [L60_도메인_랜덤화_학습_환경_구축](M8_sim2real/L60_도메인_랜덤화_학습_환경_구축/) | `01_dr.py`<br>`02_adr.py` |
| [L61_학습_정책_실물_배포_성능_검증](M8_sim2real/L61_학습_정책_실물_배포_성능_검증/) | `01_내보내기와_실행_노드.py` |
| [L62_실패_케이스_분석_보정_전략_적용](M8_sim2real/L62_실패_케이스_분석_보정_전략_적용/) | `01_sysid.py` |

#### M9_edge_deployment

| 강의 폴더 | 파일 |
|---|---|
| [L63_ONNXRuntime_추론_최적화](M9_edge_deployment/L63_ONNXRuntime_추론_최적화/) | `01_ONNX_모델의_표준_도면.py`<br>`02_ONNXRuntime_실행_공급자_EP_라는_설계.py` |
| [L67_ONNX_TensorRT_변환_FP16_INT8_양자화](M9_edge_deployment/L67_ONNX_TensorRT_변환_FP16_INT8_양자화/) | `01_export_all.py`<br>`02_컨베이어_2구간_엔진_빌드.sh`<br>`03_컨베이어_2구간_엔진_빌드.py` |
| [L68_추론_지연](M9_edge_deployment/L68_추론_지연/) | `01_profiler.py` |
| [L69_ROS2_제어_루프_통합_안정성_검증](M9_edge_deployment/L69_ROS2_제어_루프_통합_안정성_검증/) | `01_trt_inference_node_의사코드.txt`<br>`02_tree_deploy.txt` |

#### M2_kinematics_dynamics/runnable

| 경로 | 내용 |
|---|---|
| `src/transforms.py` | `rot_z`, `rot_x`, `trans`, `dh_transform` (13강) |
| `src/fk_chain.py` | `PlanarArm`, `Arm3D` (13강) |
| `src/jacobian.py` | `jacobian_planar`, `jacobian_numeric`, `singularity_metrics`, `dls`, `adaptive_lambda` (14강) |
| `src/trajectory.py` | `quintic` (15강) |
| `src/arm_dynamics.py` | `TwoLinkDynamics` — M·C·g·energy, `step`(원문), `step_rk4`(보강) (12·15강) |
| `tests/` | `test_fk.py`, `test_jacobian.py`, `test_dynamics.py` |
| `demos/` | `demo_fk_workspace.py`, `demo_singularity.py`, `demo_tracking.py` → `demos/out/*.png` |
