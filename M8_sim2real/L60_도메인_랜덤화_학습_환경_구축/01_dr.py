# [CH2 Physical AI] 60강. [실습] 도메인 랜덤화 학습 환경 구축
# 절: 1. 구현 — 리셋에 끼어드는 랜덤화
# 원본 경로: dr.py
# ※ 강의 교안의 코드 블록을 원문 그대로 옮긴 것(핵심부 발췌 포함)

# dr.py — 설정표(yaml)가 그대로 코드에 물린다
class DomainRandomizer:
    def __init__(self, cfg, seed):
        self.rng = np.random.default_rng(seed)     # 재현성!
        self.cfg = cfg                              # {param: {dist, lo, hi, enabled}}

    def sample(self, env_ids):
        """리셋되는 환경들의 ξ를 뽑아 시뮬에 적용"""
        for name, c in self.cfg.items():
            if not c.enabled: continue
            val = self.rng.uniform(c.lo, c.hi, len(env_ids))
            self.sim.set_param(name, env_ids, val)   # 질량·마찰·게인·지연·노이즈...
        self.log_xi(env_ids, ...)                    # ξ를 에피소드에 기록 (분석용!)
