from __future__ import annotations

import os
import re

import yaml

from dataset import Dataset

_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "domains.yaml"
)

# R4b (a): 투표에서 제외할 좌표·보조 변수 이름(소문자) 및 standard_name
_COORD_EXCLUDE_NAMES: frozenset = frozenset({
    "longitude", "latitude", "lon", "lat", "time",
    "tri", "element", "node", "mapsta", "depth",
})
_COORD_EXCLUDE_SNS: frozenset = frozenset({"longitude", "latitude"})

# R4b (b): 파랑 대표변수(headline) — 존재하면 waves 도메인 우선 반환
_WAVE_HEADLINE_SN = "sea_surface_wave_significant_height"
_WAVE_HEADLINE_RE = re.compile(r"^hs$|hm0|swh")


def _load_domains(path: str = _CONFIG) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["domains"]


def _match_var(var, domains: dict):
    """한 변수가 어느 도메인에 맞는지 — standard_name 우선, 없으면 이름 패턴."""
    sn = (var.standard_name or "").lower()
    name = var.name.lower()
    for dom, spec in domains.items():
        if sn and sn in [s.lower() for s in spec.get("standard_names", [])]:
            return dom
    for dom, spec in domains.items():
        for pat in spec.get("name_patterns", []):
            if re.search(pat, name):
                return dom
    return None


def _is_aux_var(var) -> bool:
    """좌표·보조 변수 여부 확인 — 투표에서 제외한다(R4b-a).

    제외 기준:
    - 이름(소문자)이 _COORD_EXCLUDE_NAMES에 속하는 변수
    - standard_name이 'longitude' 또는 'latitude'인 변수
    """
    if var.name.lower() in _COORD_EXCLUDE_NAMES:
        return True
    sn = (var.standard_name or "").lower()
    return sn in _COORD_EXCLUDE_SNS


def _is_wave_headline(var) -> bool:
    """파랑 대표변수 판정 — R4b (b).

    standard_name == sea_surface_wave_significant_height
    또는 이름이 hs / hm0 포함 / swh 포함이면 True.
    """
    sn = (var.standard_name or "").lower()
    if sn == _WAVE_HEADLINE_SN:
        return True
    return bool(_WAVE_HEADLINE_RE.search(var.name.lower()))


def detect_domain(d: Dataset, domains: dict | None = None) -> dict:
    if domains is None:
        domains = _load_domains()
    variables = d.variables()

    # R4b (a): 좌표·보조 변수 제외 후 물리 변수만 투표에 참여
    phys_vars = {n: v for n, v in variables.items() if not _is_aux_var(v)}

    matched: dict = {}
    has_wave_headline = False
    for name, var in phys_vars.items():
        # R4b (b): 파랑 headline 감지
        if _is_wave_headline(var):
            has_wave_headline = True
        dom = _match_var(var, domains)
        if dom is not None:
            matched[name] = dom

    if not matched and not has_wave_headline:
        return {"domain": "unknown", "confidence": 0.0, "matched": {}}

    # R4b (b): 파랑 headline 존재 시 waves 우선 반환
    if has_wave_headline:
        wave_count = sum(1 for dom in matched.values() if dom == "waves")
        confidence = max(wave_count, 1) / max(1, len(phys_vars))
        return {"domain": "waves", "confidence": round(confidence, 3), "matched": matched}

    # 최다 득표 도메인 (파랑 headline 없는 일반 경우)
    counts: dict = {}
    for dom in matched.values():
        counts[dom] = counts.get(dom, 0) + 1
    best = max(counts, key=counts.get)
    confidence = counts[best] / max(1, len(phys_vars))
    return {"domain": best, "confidence": round(confidence, 3), "matched": matched}
