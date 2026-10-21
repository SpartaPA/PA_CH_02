#!/usr/bin/env bash
# [CH2 Physical AI] 52강. [실습] Diffusion Policy 비정형 조작 학습
# 절: 1. 갈림길 데이터셋 — 저주를 설계하다
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

python collector.py --obstacle --episodes 60 --strategy alternate
#  물체는 장애물 건너편, 시연자는 회차마다 좌/우 교대로 회피 (팀원 2명이 각자 선호 전략이면 더 자연스러움)
