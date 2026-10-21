# [CH2 Physical AI] 51강. [실습] MLP/CNN/Transformer BC 정책 학습
# 절: 1. 학습기 골격 — 재사용 가능한 한 벌
# 원본 경로: train_bc.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# train_bc.py — 아키텍처만 갈아 끼우는 공용 학습기
def train(model, cfg):
    ds = DemoDataset("demos_clean.hdf5", split="train")     # 동결 분할 사용
    dl = DataLoader(ds, batch_size=256, shuffle=True)
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr)
    for epoch in range(cfg.epochs):
        for obs, act in dl:
            loss = F.mse_loss(model(obs), act)
            opt.zero_grad(); loss.backward(); opt.step()
        val = evaluate_mse(model, split="val")
        save_if_best(model, val)                             # 체크포인트
        log(epoch, loss, val)                                # csv — 곡선의 원천
