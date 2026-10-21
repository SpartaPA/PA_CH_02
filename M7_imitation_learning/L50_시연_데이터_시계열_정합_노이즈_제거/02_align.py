# [CH2 Physical AI] 50강. [실습] 시연 데이터 시계열 정합·노이즈 제거
# 절: 2. 정합 — 다주기 스트림을 (o, a) 짝으로
# 원본 경로: align.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# align.py (핵심)
def align_episode(state, action, scene, hz=20):
    t_grid = np.arange(t0, t1, 1/hz)
    th  = interp_linear(state.t,  state.theta,  t_grid)   # 연속량: 선형 보간
    thd = interp_linear(state.t,  state.dtheta, t_grid)
    obj = hold_last(scene.t, scene.obj, t_grid)           # 저주기: 최근값 유지
    act = hold_last(action.t, action.cmd, t_grid)         # 명령: 계단(보간 금지!)
    return np.column_stack([th, thd, obj]), act
