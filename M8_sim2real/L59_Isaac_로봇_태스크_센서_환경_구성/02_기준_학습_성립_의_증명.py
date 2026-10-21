# [CH2 Physical AI] 59강. [실습] Isaac 로봇 태스크·센서 환경 구성
# 절: 4. 기준 학습 — "성립"의 증명
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# 학습 중 상주 평가 (58강 관행의 배선) — 오늘부터 붙입니다
if step % EVAL_EVERY == 0:
    log("train_sr", eval_on(env_train))       # 훈련 조건
    log("proxy_sr", eval_on(env_proxy))       # 모의 실물 (57강 실습 1의 그 환경!)
