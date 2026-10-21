# [CH2 Physical AI] 15강. [실습] Quintic 궤적 생성 + PID 튜닝
# 절: 3. 추종 실험 — 계단 vs Quintic, PID vs PID+중력 보상
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

tau = Kp*(th_ref - th) + Kd*(thd_ref - thd) + Ki*integ    # 관절별 PID
tau += sim.gvec(th)                                        # (나) 중력 보상 켜기
