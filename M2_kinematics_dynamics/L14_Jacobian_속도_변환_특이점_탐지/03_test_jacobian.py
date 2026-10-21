# [CH2 Physical AI] 14강. [실습] Jacobian 속도 변환·특이점 탐지
# 절: 1-2. 수치 미분 Jacobian — 검증자
# 원본 경로: tests/test_jacobian.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# tests/test_jacobian.py — 두 구현의 교차 검증
@pytest.mark.parametrize("thetas", [(0.1, 0.5), (1.2, -0.7), (0.0, 1.57)])
def test_analytic_matches_numeric(thetas):
    arm = PlanarArm([0.3, 0.2])
    Ja = jacobian_planar(arm.L, thetas)
    Jn = jacobian_numeric(arm.fk, thetas)
    np.testing.assert_allclose(Ja, Jn, atol=1e-6)
