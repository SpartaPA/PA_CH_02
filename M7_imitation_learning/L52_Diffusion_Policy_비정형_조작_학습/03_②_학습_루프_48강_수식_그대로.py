# [CH2 Physical AI] 52강. [실습] Diffusion Policy 비정형 조작 학습
# 절: ② 학습 루프 — 48강 수식 그대로
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

for obs, act_seq in dl:                     # act_seq: (B, H, 2) — 시퀀스 단위 샘플!
    k = torch.randint(0, K, (B,))
    eps = torch.randn_like(act_seq)
    noisy = sqrt_ab[k] * act_seq + sqrt_1mab[k] * eps    # 정과정 (닫힌 식)
    loss = F.mse_loss(model(noisy, k, obs), eps)          # 노이즈를 맞혀라
