# [CH2 Physical AI] 52강. [실습] Diffusion Policy 비정형 조작 학습
# 절: ③ 샘플링과 리시딩 호라이즌 실행
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

def sample_action_seq(obs, K=50):
    a = torch.randn(1, H, 2)
    for k in reversed(range(K)):
        a = denoise_step(a, model(a, k, obs), k)      # DDPM 역과정 한 스텝
    return a                                           # (H, 2) 행동 시퀀스

# 실행 루프: 생성 → 앞 h=8 스텝 실행 → 새 관측 → 재생성 (48강 ③)
