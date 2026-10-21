# [CH2 Physical AI] 22강. [실습] 검출→포즈추정 비전 파이프라인 통합
# 절: 2. 경로 A — ArUco → PnP → PoseStamped
# 원본 경로: aruco_pose_node.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# aruco_pose_node.py (핵심부)
self.detector = cv2.aruco.ArucoDetector(
    cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50))
MARKER = 0.05                                  # 마커 한 변 실측 [m]
OBJ = np.array([[-1, 1, 0], [1, 1, 0], [1, -1, 0], [-1, -1, 0]], np.float32) * MARKER / 2

def on_image(self, msg):
    if self.K is None:                          # /camera_info에서 수신 대기
        return
    frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
    corners, ids, _ = self.detector.detectMarkers(frame)
    if ids is None:
        return
    ok, rvec, tvec = cv2.solvePnP(OBJ, corners[0], self.K, self.dist)
    if not ok:
        return
    err = self.reproj_error(OBJ, corners[0], rvec, tvec)     # 18강 검증 습관
    if err > 2.0:                               # px — 나쁜 포즈는 발행하지 않는다
        self.get_logger().warn(f"reproj {err:.1f}px — drop")
        return
    self.pub.publish(self.to_pose_stamped(rvec, tvec, msg.header))
