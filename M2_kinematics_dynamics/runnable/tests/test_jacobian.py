# tests/test_jacobian.py — 두 구현의 교차 검증 (14강)
import numpy as np
import pytest
from src.fk_chain import PlanarArm
from src.jacobian import jacobian_planar, jacobian_numeric, singularity_metrics

# tests/test_jacobian.py — 두 구현의 교차 검증
@pytest.mark.parametrize("thetas", [(0.1, 0.5), (1.2, -0.7), (0.0, 1.57)])
def test_analytic_matches_numeric(thetas):
    arm = PlanarArm([0.3, 0.2])
    Ja = jacobian_planar(arm.L, thetas)
    Jn = jacobian_numeric(arm.fk, thetas)
    np.testing.assert_allclose(Ja, Jn, atol=1e-6)


def test_singularity_detected_when_arm_straight():
    # 팔을 쭉 편 자세(theta2 = 0)는 2링크 평면 팔의 경계 특이점
    J = jacobian_planar([0.3, 0.2], (0.4, 0.0))
    m = singularity_metrics(J)
    assert m["manipulability"] < 1e-6   # sqrt(det) 이라 수치 잔차가 커 보임
    assert m["sigma_min"] < 1e-12
