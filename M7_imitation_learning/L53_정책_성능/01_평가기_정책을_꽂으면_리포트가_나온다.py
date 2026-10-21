# [CH2 Physical AI] 53강. [실습] 정책 성능(Success Rate·Smoothness) 검증
# 절: 1. 평가기 — 정책을 꽂으면 리포트가 나온다
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# policy_eval/ — 공용 평가 패키지
#  interface: policy(obs) -> action  (BC든 DP든 이 규약만 맞추면 평가 가능)
#  runner:  조건 격자 x 반복 x 시드 롤아웃 (45강 bench_runner의 정책판)
#  judge:   성공 4조건 (도달 반경·시간 한도·충돌 없음·관절 한계 내)
#  metrics: success(+Wilson CI), 도달 시간, jerk RMS, 행동 변화량, 경로 길이비
#  report:  대시보드 그림 + yaml 결과 (커밋 해시·설정 포함)
