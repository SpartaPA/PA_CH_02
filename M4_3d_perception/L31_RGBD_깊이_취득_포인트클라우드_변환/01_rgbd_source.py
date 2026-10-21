# [CH2 Physical AI] 31강. [실습] RGBD 깊이 취득·포인트클라우드 변환
# 절: 1. 취득 — 정렬된 두 이미지
# 원본 경로: src/rgbd_source.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# src/rgbd_source.py (RealSense 경로)
import pyrealsense2 as rs

class RealSenseSource:
    def __init__(self, w=640, h=480, fps=30):
        self.pipe = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.color, w, h, rs.format.bgr8, fps)
        cfg.enable_stream(rs.stream.depth, w, h, rs.format.z16, fps)
        prof = self.pipe.start(cfg)
        self.align = rs.align(rs.stream.color)          # 27강의 그 정렬!
        i = prof.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
        self.K = np.array([[i.fx, 0, i.ppx], [0, i.fy, i.ppy], [0, 0, 1]])
        self.depth_scale = prof.get_device().first_depth_sensor().get_depth_scale()

    def read(self):
        fr = self.align.process(self.pipe.wait_for_frames())
        color = np.asanyarray(fr.get_color_frame().get_data())
        depth = np.asanyarray(fr.get_depth_frame().get_data()) * self.depth_scale  # [m]
        return color, depth                              # depth: (H, W) float, 0 = 무효
