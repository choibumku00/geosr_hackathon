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
    sn = (var.standard_name or "").lower()
    if sn and sn in [s.lower() for s in rule.get("standard_names", [])]:
        return True
    name = var.name.lower()
    for pat in rule.get("name_patterns", []):
        if re.search(pat, name):
            return True
    units = (var.units or "").strip()
    if units and units in rule.get("units_any", []):
        return True
    return False


def match_rule(var: Variable, rules: dict | None = None) -> dict | None:
    if rules is None:
        rules = load_rules()
    for rule in rules["rules"]:
        if _identity_match(var, rule) and _units_ok(var, rule):
            return rule
    return None
