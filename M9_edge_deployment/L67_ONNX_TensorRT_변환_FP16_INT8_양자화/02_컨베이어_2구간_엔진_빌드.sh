#!/usr/bin/env bash
# [CH2 Physical AI] 67강. [실습] ONNX→TensorRT 변환·FP16/INT8 양자화
# 절: 2. 컨베이어 2구간 — 엔진 빌드
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# FP32 / FP16
trtexec --onnx=yolo.onnx --saveEngine=yolo_fp32.engine
trtexec --onnx=yolo.onnx --fp16 --saveEngine=yolo_fp16.engine
# INT8 (캘리브레이터는 파이썬 API로 — 아래)
