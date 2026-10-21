# tests/test_fk.py
import numpy as np
import pytest
from src.fk_chain import PlanarArm

arm = PlanarArm([0.3, 0.2])
CASES = [((0, 0), (0.5, 0.0)),
         ((np.pi/2, 0), (0.0, 0.5)),
         ((0, np.pi/2), (0.3, 0.2)),
         ((np.pi/2, -np.pi/2), (0.2, 0.3)),
         ((np.pi/4, np.pi/4), (0.3*np.cos(np.pi/4), 0.3*np.sin(np.pi/4)+0.2))]

@pytest.mark.parametrize("thetas, expected", CASES)
def test_fk_known_poses(thetas, expected):
    np.testing.assert_allclose(arm.fk(thetas), expected, atol=1e-12)

def test_fk_3dof_matches_formula():
    arm3 = PlanarArm([0.3, 0.2, 0.1])
    th = np.array([0.3, -0.4, 0.9])
    cum = np.cumsum(th)
    expected = (np.sum(arm3.L * np.cos(cum)), np.sum(arm3.L * np.sin(cum)))
    np.testing.assert_allclose(arm3.fk(th), expected, atol=1e-12)
