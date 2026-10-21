# [CH2 Physical AI] 13강. [실습] 2~3DOF FK 동차변환 체인
# 절: 4-2. 작업 공간 — FK를 몬테카를로로
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

rng = np.random.default_rng(0)
ths = rng.uniform(-np.pi, np.pi, size=(20000, 2))
pts = np.array([arm.fk(t) for t in ths])          # (실습: 벡터화해 보세요)
plt.scatter(pts[:, 0], pts[:, 1], s=1, alpha=0.2)
