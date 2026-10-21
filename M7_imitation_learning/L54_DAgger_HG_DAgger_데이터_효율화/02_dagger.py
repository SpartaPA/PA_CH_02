# [CH2 Physical AI] 54강. [실습] DAgger/HG-DAgger 데이터 효율화
# 절: 2. DAgger 루프 — 라운드가 곡선을 만든다
# 원본 경로: dagger.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# dagger.py
D = load("demos_clean.hdf5")                     # 초기 시연 (50강)
for round in range(R):
    pi = train_bc(D)                              # 51강 학습기 재사용
    states = rollout_collect(pi, n_episodes=20)   # 정책이 방문한 상태들
    labels = [(o, expert_action(o)) for o in states]   # 전문가 재라벨
    D = D + labels                                # 집계(aggregate)
    eval_report(pi, round)                        # 53강 평가기 재사용
