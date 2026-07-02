from __future__ import annotations

import os
import re

import yaml

from dataset import Variable

_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "rules.yaml"
)


def load_rules(path: str | None = None) -> dict:
    with open(path or _CONFIG, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data.setdefault("rules", [])
    data.setdefault("default", {})
    return data


def _units_ok(var: Variable, rule: dict) -> bool:
    units_any = rule.get("units_any")
    if not units_any:
        return True
    if var.units is None:
        return True  # 변수에 단위가 없으면 단위 제약을 적용하지 않음
    return var.units.strip() in units_any


def _identity_match(var: Variable, rule: dict) -> bool:
    """변수 '정체' 매칭은 standard_name 또는 name_pattern 으로만 한다.

    units_any 는 정체 신호가 아니라 '필터'(_units_ok)로만 쓴다 — 단위(K 등)만
    같다고 규칙을 태우면, 온도가 아닌데 K를 쓰는 변수가 온도 규칙에 오탐된다.
    (범용 검증에서 위험 → units 단독 매칭 금지.)
    """
    sn = (var.standard_name or "").lower()
    if sn and sn in [s.lower() for s in rule.get("standard_names", [])]:
        return True
    name = var.name.lower()
    for pat in rule.get("name_patterns", []):
        if re.search(pat, name):
            return True
    return False


def match_rule(var: Variable, rules: dict | None = None) -> dict | None:
    if rules is None:
        rules = load_rules()
    for rule in rules["rules"]:
        if _identity_match(var, rule) and _units_ok(var, rule):
            return rule
    return None
