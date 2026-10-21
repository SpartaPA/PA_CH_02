# [CH2 Physical AI] 23강. 카메라 좌표계 변환 심화 (World/Camera/Image/Pixel·Extrinsic/Intrinsic)
# 절: 3. 사슬 왕복 — 코드로 검증
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

def project(P_w, K, R, t):                    # 정방향: 3D → 픽셀
    P_c = R @ P_w + t
    if P_c[2] <= 0:                            # 카메라 뒤!
        return None
    uv = K @ (P_c / P_c[2])
    return uv[:2]

def backproject(u, v, Z, K, R, t):            # 역방향: 픽셀+깊이 → 3D
    x_n = (u - K[0, 2]) / K[0, 0]
    y_n = (v - K[1, 2]) / K[1, 1]
    P_c = Z * np.array([x_n, y_n, 1.0])       # 광선 × 깊이
    return R.T @ (P_c - t)                     # Camera → World (역변환!)

# 왕복: P_w → (u,v,Z) → P_w' 가 원본과 일치해야 한다
P2 = backproject(*project(P_w, K, R, t), Z=(R @ P_w + t)[2], K=K, R=R, t=t)
assert np.allclose(P_w, P2, atol=1e-9)
