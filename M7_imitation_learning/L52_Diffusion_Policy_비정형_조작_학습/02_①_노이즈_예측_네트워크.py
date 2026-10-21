# [CH2 Physical AI] 52강. [실습] Diffusion Policy 비정형 조작 학습
# 절: ① 노이즈 예측 네트워크
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

class NoisePredictor(nn.Module):
    """입력: 노이즈 낀 행동 시퀀스 a^k (H,2), 스텝 k, 관측 o(6)  → 노이즈 예측 (H,2)"""
    def __init__(self, H=16, d=256):
        self.obs_enc  = nn.Sequential(nn.Linear(6, d), nn.ReLU())
        self.k_emb    = SinusoidalEmb(d)              # 스텝 임베딩
        self.backbone = nn.Sequential(                 # 1D Conv U-Net 소형판
            Conv1dBlock(2, 64), Conv1dBlock(64, 128), Conv1dBlock(128, 64),
            nn.Conv1d(64, 2, 1))
        # obs·k 임베딩은 FiLM(스케일·시프트)으로 각 블록에 조건 주입
