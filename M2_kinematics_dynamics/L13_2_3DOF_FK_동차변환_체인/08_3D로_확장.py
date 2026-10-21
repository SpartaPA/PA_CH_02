# [CH2 Physical AI] 13강. [실습] 2~3DOF FK 동차변환 체인
# 절: 4-3. 3D로 확장
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# z축 오프셋이 있는 3DOF (베이스 회전 + 평면 2링크): D-H로는 alpha=90° 한 행 추가
class Arm3D(PlanarArm):
    def fk_all(self, thetas):
        T = dh_transform(thetas[0], 0.15, 0.0, np.pi/2)   # 허리 회전
        Ts = [T]
        for L, th in zip(self.L, thetas[1:]):
            T = T @ dh_transform(th, 0.0, L, 0.0)
            Ts.append(T)
        return Ts
