# [CH2 Physical AI] 67강. [실습] ONNX→TensorRT 변환·FP16/INT8 양자화
# 절: 2. 컨베이어 2구간 — 엔진 빌드
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# INT8 캘리브레이션 (파이썬 API 핵심)
class Calibrator(trt.IInt8EntropyCalibrator2):
    def get_batch(self, names):
        return [next(self.data_iter)]        # 대표 데이터 300~500 샘플
# builder 설정: config.set_flag(trt.BuilderFlag.INT8); config.int8_calibrator = ...
