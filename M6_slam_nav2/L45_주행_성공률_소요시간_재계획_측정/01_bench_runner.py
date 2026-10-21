# [CH2 Physical AI] 45강. [실습] 주행 성공률·소요시간·재계획 측정
# 절: 2. 벤치마크 러너 — 대량 반복의 자동화
# 원본 경로: bench_runner.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# bench_runner.py outline
# 1. Reset Isaac Sim USD scene and robot spawn using fixed/random seeds.
# 2. Reset simulation-time consumers, load cuVSLAM map, provide pose hint.
# 3. Verify localization and TF; restore nvblox state and activate Nav2.
# 4. Run patrol with rosbag/logger; score collision/intervention/time/goals.
# 5. Save run results; aggregate distributions and failure causes.
