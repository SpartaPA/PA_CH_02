# [CH2 Physical AI] 54강. [실습] DAgger/HG-DAgger 데이터 효율화
# 절: 1. 자동 전문가 — 라벨러의 자격
# 원본 경로: expert.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# expert.py — 어느 상태에서든 정답 행동을 주는 스크립트 전문가
def expert_action(obs):
    """CLIK(14강) + 장애물 반발 휴리스틱: 목표 방향 속도 - 장애물 척력 → IK → 관절 델타"""
