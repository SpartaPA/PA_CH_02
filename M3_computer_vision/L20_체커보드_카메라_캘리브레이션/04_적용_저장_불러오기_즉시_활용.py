# [CH2 Physical AI] 20강. [실습] 체커보드 카메라 캘리브레이션 (intrinsic/distortion)
# 절: 4. 적용 — 저장·불러오기·즉시 활용
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

d = np.load("camera_params.npz")
K, dist = d["K"], d["dist"]
