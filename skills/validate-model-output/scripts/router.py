from __future__ import annotations

import os
import re

import yaml

from dataset import Dataset

_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "domains.yaml"
)


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


def detect_domain(d: Dataset, domains: dict | None = None) -> dict:
    if domains is None:
        domains = _load_domains()
    variables = d.variables()
    matched = {}
    for name, var in variables.items():
        dom = _match_var(var, domains)
        if dom is not None:
            matched[name] = dom
    if not matched:
        return {"domain": "unknown", "confidence": 0.0, "matched": {}}
    # 최다 득표 도메인
    counts = {}
    for dom in matched.values():
        counts[dom] = counts.get(dom, 0) + 1
    best = max(counts, key=counts.get)
    confidence = counts[best] / max(1, len(variables))
    return {"domain": best, "confidence": round(confidence, 3), "matched": matched}
