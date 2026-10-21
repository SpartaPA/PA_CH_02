# [CH2 Physical AI] 54강. [실습] DAgger/HG-DAgger 데이터 효율화
# 절: 3. HG-DAgger — 사람이 게이트가 되다
# 원본 경로: hg_dagger.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# hg_dagger.py — 개입 이벤트: (시작 t, 종료 t, 구간 (o, a*) 목록)
# 라운드: 정책 실행 20 에피소드 감독 → 개입 데이터 집계 → 재학습 → 반복
