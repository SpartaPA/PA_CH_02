# tests/test_dynamics.py — 15강 시뮬레이터 검증
import numpy as np
from src.arm_dynamics import TwoLinkDynamics
from src.trajectory import quintic


def test_energy_conservation_without_damping():
    # 교안 원문은 sim.step(오일러)으로 1e-2를 기대하지만, 이 자세에서 5초 자유 진동은
    # 오일러로 약 25% 에너지가 빠진다 → 적분기 오차와 모델 오류를 구분하기 위해 RK4로 검증
    sim = TwoLinkDynamics(); sim.th = np.array([0.3, 0.5])
    E0 = sim.energy()
    for _ in range(5000): sim.step_rk4(np.zeros(2))
    assert abs(sim.energy() - E0) / abs(E0) < 1e-6


def test_mass_matrix_symmetric_positive_definite():
    sim = TwoLinkDynamics()
    for th2 in np.linspace(-np.pi, np.pi, 13):
        M = sim.M(np.array([0.0, th2]))
        np.testing.assert_allclose(M, M.T)
        assert np.all(np.linalg.eigvalsh(M) > 0)


def test_gravity_compensation_holds_pose():
    sim = TwoLinkDynamics(); sim.th = np.array([0.0, 0.0])   # 수평으로 뻗은 팔
    for _ in range(1000): sim.step(sim.gvec(sim.th))
    np.testing.assert_allclose(sim.th, 0.0, atol=1e-9)


def test_quintic_boundary_conditions():
    f = quintic(0.0, 1.0, 2.0)
    p0, v0, a0 = f(0.0); pT, vT, aT = f(2.0)
    np.testing.assert_allclose([p0, v0, a0, pT, vT, aT], [0, 0, 0, 1, 0, 0], atol=1e-12)
