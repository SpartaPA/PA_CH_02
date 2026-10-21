# [CH2 Physical AI] 47강. Behavior Cloning 정책 학습
# 절: 4. 우리의 실습 무대 — 2링크 도달 과제 (51강 예열)
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# 정책 (저차원 버전) — 이것이 전부입니다
policy = nn.Sequential(nn.Linear(6, 128), nn.ReLU(),
                       nn.Linear(128, 128), nn.ReLU(),
                       nn.Linear(128, 2))
loss = F.mse_loss(policy(obs), action)
