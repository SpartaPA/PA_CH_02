# [CH2 Physical AI] 13강. [실습] 2~3DOF FK 동차변환 체인
# 절: 4-1. 자세 그리기
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

def draw_arm(ax, arm, thetas, **kw):
    pts = np.array([[0, 0]] + [T[:2, 3] for T in arm.fk_all(thetas)])
    ax.plot(pts[:, 0], pts[:, 1], "-o", lw=3, ms=8, **kw)
