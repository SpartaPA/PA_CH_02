# [CH2 Physical AI] 55강. Isaac Sim/Isaac Lab 태스크 구성 (USD Asset·Sensor)
# 절: 병렬성 — 이 도구의 존재 이유
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# Isaac Lab 스타일 의사코드 — 인터페이스 감각
env = TaskEnv(num_envs=4096, device="cuda")
obs = env.reset()                        # (4096, obs_dim)
for step in range(horizon):
    act = policy(obs)                    # (4096, act_dim) — 정책도 배치로!
    obs, reward, done, info = env.step(act)
