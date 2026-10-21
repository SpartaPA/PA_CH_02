# [CH2 Physical AI] 29강. [실습] YOLO 추론 ROS2 통합
# 절: 1. 노드 설계 — 표준 메시지로 말하기
# 원본 경로: yolo_node.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# yolo_node.py (핵심부)
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose

class YoloNode(Node):
    def __init__(self):
        super().__init__("yolo_detector")
        self.declare_parameter("model", "yolov8n.pt")
        self.declare_parameter("conf", 0.5)
        self.declare_parameter("iou", 0.45)          # 25강의 두 손잡이 → ROS 파라미터
        self.model = YOLO(self.get_parameter("model").value)
        self.latest = None                            # 최신 프레임 슬롯 (드롭 정책!)
        self.sub = self.create_subscription(Image, "/image_raw", self.on_image,
                                            qos_profile_sensor_data)
        self.timer = self.create_timer(0.01, self.on_timer)   # 처리 루프 분리
        self.pub = self.create_publisher(Detection2DArray, "/detections", 10)

    def on_image(self, msg):
        self.latest = msg                             # 저장만 — 콜백은 가볍게

    def on_timer(self):
        if self.latest is None:
            return
        msg, self.latest = self.latest, None          # 최신만 꺼내 처리
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        results = self.model(frame, conf=self.get_parameter("conf").value,
                             iou=self.get_parameter("iou").value, verbose=False)
        out = Detection2DArray(); out.header = msg.header     # 스탬프 계승!
        for b in results[0].boxes:
            det = Detection2D()
            det.bbox.center.position.x = float((b.xyxy[0][0] + b.xyxy[0][2]) / 2)
            det.bbox.center.position.y = float((b.xyxy[0][1] + b.xyxy[0][3]) / 2)
            det.bbox.size_x = float(b.xyxy[0][2] - b.xyxy[0][0])
            det.bbox.size_y = float(b.xyxy[0][3] - b.xyxy[0][1])
            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = self.model.names[int(b.cls)]
            hyp.hypothesis.score = float(b.conf)
            det.results.append(hyp)
            out.detections.append(det)
        self.pub.publish(out)
