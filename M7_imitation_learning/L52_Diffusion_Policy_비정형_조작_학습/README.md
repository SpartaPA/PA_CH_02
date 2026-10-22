# [52강. [실습] Diffusion Policy 비정형 조작 학습]
- 모듈: ⑦ 로봇 모방학습 및 정책 최적화
- 한 줄 요약: 장애물을 좌/우로 돌아가는 다봉 시연 데이터를 일부러 만들고, 노이즈 예측 네트워크·DDPM 학습·역과정 샘플링·리시딩 호라이즌 실행으로 Diffusion Policy를 구현

## [핵심 개념]
- **다봉 행동 분포의 함정** → 같은 관측에 정답이 좌·우 두 개면 MSE 최적해는 평균 = 장애물 정면(충돌 경로)
- **확산 순방향(닫힌 식)** → $a_k=\sqrt{\bar\alpha_k}\,a_0+\sqrt{1-\bar\alpha_k}\,\epsilon,\ \epsilon\sim\mathcal N(0,I)$
  - $\bar\alpha_k=\prod_{s\le k}(1-\beta_s)$, $k$가 클수록 순수 노이즈에 가까움
- **학습 목적** → $\mathcal L=\mathbb E_{k,\epsilon}\,\|\epsilon-\epsilon_\theta(a_k,k,o)\|^2$ (노이즈 예측)
- **역과정(DDPM 한 스텝)** → $a_{k-1}=\frac{1}{\sqrt{\alpha_k}}\Big(a_k-\frac{\beta_k}{\sqrt{1-\bar\alpha_k}}\epsilon_\theta\Big)+\sigma_k z$
  - 무작위 시작점 $a_K\sim\mathcal N(0,I)$에 따라 서로 다른 봉우리(좌/우)를 샘플 → 평균으로 뭉개지지 않음
- **행동 시퀀스 예측** → 한 스텝이 아니라 $H$ 스텝 묶음 $(H,2)$를 생성 → 시간적 일관성(중간에 좌↔우 전환 방지)
- **조건 주입(FiLM)** → 관측·스텝 임베딩으로 특징맵에 스케일·시프트 $\gamma\odot h+\beta$
- **사인파 스텝 임베딩** → 정수 $k$를 다중 주파수 $\sin/\cos$ 벡터로
- **리시딩 호라이즌** → $H$ 생성 후 앞 $h$만 실행 → 새 관측으로 재생성, 반응성과 일관성의 절충

## [파일별 내용]
- `01_갈림길_데이터셋_저주를_설계하다.sh` — `collector.py --obstacle --episodes 60 --strategy alternate`
  - 물체는 장애물 건너편, 회차마다 좌/우 교대 회피 → 의도적 다봉 데이터
- `02_①_노이즈_예측_네트워크.ipynb` — `NoisePredictor(H=16, d=256)`
  - 입력: 노이즈 행동 시퀀스 $a^k$ `(H,2)`, 스텝 `k`, 관측 `o(6)` → 출력: 노이즈 `(H,2)`
  - `obs_enc`(Linear 6→d), `k_emb = SinusoidalEmb(d)`
  - `backbone`: `Conv1dBlock(2,64)→(64,128)→(128,64)→Conv1d(64,2,1)`, 시간축 1D 합성곱 U-Net 소형판
  - 빠진 맥락: `super().__init__()`, `forward`, `SinusoidalEmb`·`Conv1dBlock`·FiLM 구현, U-Net 스킵 연결
- `03_②_학습_루프_48강_수식_그대로.ipynb` — 학습 한 배치
  - `act_seq`: `(B,H,2)` 시퀀스 단위 샘플
  - `k = randint(0,K,(B,))`, `eps = randn_like`, `noisy = sqrt_ab[k]*act_seq + sqrt_1mab[k]*eps`
  - `loss = mse_loss(model(noisy,k,obs), eps)`
  - 주의: `sqrt_ab[k]`는 `(B,)` → `(B,1,1)`로 reshape해야 브로드캐스트 정상, 옵티마이저 스텝 생략됨
- `04_③_샘플링과_리시딩_호라이즌_실행.ipynb` — `sample_action_seq(obs, K=50)`
  - `a = randn(1,H,2)` → `k = K-1 … 0` 역순으로 `denoise_step` 반복 → `(H,2)` 반환
  - 실행 루프: 생성 → 앞 `h=8` 스텝 실행 → 새 관측 → 재생성
  - `denoise_step`은 위 DDPM 역과정 식(구현 생략)

## [선수 지식·연결]
- 48강: 확산 수식·리시딩 호라이즌 이론, 47·51강: MSE 기반 BC(비교 기준선)
- 50강: 수집기·정합 파이프라인 재사용(단, 시퀀스 샘플 `(H,2)`로 데이터셋 구성 필요)
- 53강: BC와 같은 평가기로 성공률·Smoothness 비교

## [실행 전 준비]
- `torch`, `h5py`, `numpy`, GPU 권장
- 노이즈 스케줄 $\beta_k$와 `sqrt_ab`, `sqrt_1mab` 사전 계산 테이블

## [확인 포인트]
- 기대 결과: 같은 관측에서 여러 번 샘플 시 좌/우 두 경로가 모두 나옴, BC(MSE)는 정면 충돌 경향
- 흔한 실수: 학습·샘플링의 `K` 불일치, 행동 정규화 범위와 노이즈 스케일 불일치, 매 스텝 재생성으로 좌↔우 진동
- 점검 질문
  - MSE BC가 이 데이터에서 실패하는 이유를 수식으로 설명할 수 있는가?
  - `h`를 1로 줄이거나 `H`로 늘리면 각각 어떤 문제가 생기는가?
  - `K=50` 샘플링 지연은 제어 주기 20 Hz와 양립하는가?
