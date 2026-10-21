# [CH2 Physical AI] 22강. [실습] 검출→포즈추정 비전 파이프라인 통합
# 절: 3. 경로 B — 색 검출 → 거리 추정
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

Z = self.fx * BALL_DIAMETER / (2.0 * r_px)          # 아는 크기로 깊이
x = (cx - self.cx) * Z / self.fx                     # 역투영 (17강 사슬의 역방향)
y = (cy - self.cy) * Z / self.fy
