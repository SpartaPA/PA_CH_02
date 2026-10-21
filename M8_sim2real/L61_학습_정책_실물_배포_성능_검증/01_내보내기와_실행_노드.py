# [CH2 Physical AI] 61강. [실습] 학습 정책 실물 배포·성능 검증
# 절: 내보내기와 실행 노드
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# 1) 정책 내보내기 — 추론만 남긴다
torch.onnx.export(policy, dummy_obs, "dr_policy.onnx")   # (모듈 ⑨의 정식 주제를 미리 한 입)

# 2) 실행 노드 (ROS2) — 모듈 ⑤ control 노드의 정책판
#   구독: /joint_states (실물 θ, θ̇)   발행: /joint_target (20Hz)
#   내부: obs 조립 → normalize(50강 stats!) → onnx 추론 → denormalize → 클램프 → 발행
