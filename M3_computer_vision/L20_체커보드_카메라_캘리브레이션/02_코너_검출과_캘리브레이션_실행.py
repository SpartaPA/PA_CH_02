# [CH2 Physical AI] 20강. [실습] 체커보드 카메라 캘리브레이션 (intrinsic/distortion)
# 절: 2. 코너 검출과 캘리브레이션 실행
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)


obj_pts, img_pts = [], []
for path in glob.glob("shots/*.jpg"):
    img = cv2.imread(path); gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ok, corners = cv2.findChessboardCorners(gray, CB)
    if not ok:
        print("코너 실패:", path); continue
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                               (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-3))
    obj_pts.append(objp); img_pts.append(corners)

rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_pts, img_pts,
                                                 gray.shape[::-1], None, None)
print("RMS 재투영 오차:", rms)                 # ← 오늘의 성적표
np.savez("camera_params.npz", K=K, dist=dist, rms=rms, image_size=gray.shape[::-1])
