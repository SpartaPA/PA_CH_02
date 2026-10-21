# [CH2 Physical AI] 15강. [실습] Quintic 궤적 생성 + PID 튜닝
# 절: 2. 시뮬레이터 — 12강 동역학을 코드로
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

def test_energy_conservation_without_damping():
    sim = TwoLinkDynamics(); sim.th = np.array([0.3, 0.5])
    E0 = sim.energy()
    for _ in range(5000): sim.step(np.zeros(2))
    assert abs(sim.energy() - E0) / abs(E0) < 1e-2   # 오일러 적분 오차 내
