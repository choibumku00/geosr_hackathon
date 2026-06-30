"""변수 별칭(alias) → CF 표준명 변환 유틸리티.

SAMPLE — 실데이터에선 구조를 실시간 점검하고
도메인 맞춤 코드로 적응하라.
헤더·변수명이 다르면 config/aliases.yaml 에 항목을 추가한다.

사용 예::

    from aliases import to_standard
    to_standard('유의파고(m)')   # → 'significant_wave_height'
    to_standard('UGRD')          # → 'eastward_wind'
    to_standard('알수없음')      # → None
"""
from __future__ import annotations

import os
import re

import yaml

# config/aliases.yaml 경로 (scripts/ → 상위 → config/)
_ALIASES_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "aliases.yaml"
)

# 단위 괄호 패턴: (m), (°C), (sec), (deg), (m/s) 등
_UNIT_BRACKET = re.compile(r"\([^)]*\)\s*$")


def load_aliases(path: str = _ALIASES_CONFIG) -> dict[str, list[str]]:
    """aliases.yaml 을 읽어 {표준명: [별칭...]} 딕셔너리로 반환한다.

    Args:
        path: YAML 파일 경로 (기본값: config/aliases.yaml).

    Returns:
        표준명 → 별칭 목록 매핑. 파일 누락 시 빈 딕셔너리.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("aliases", {}) or {}
    except FileNotFoundError:
        return {}


# 모듈 로드 시 한 번 빌드: {소문자 별칭 → 표준명}
def _build_lookup(aliases: dict[str, list[str]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for std, alias_list in aliases.items():
        for alias in alias_list:
            lookup[alias.lower()] = std
    return lookup


_LOOKUP: dict[str, str] = _build_lookup(load_aliases())


def to_standard(name_or_header: str, lookup: dict[str, str] | None = None) -> str | None:
    """변수명 또는 CSV 헤더 문자열을 CF 표준명으로 변환한다.

    처리 순서:
    1. 한글 헤더에서 단위 괄호 제거 (예: ``유의파고(m)`` → ``유의파고``).
    2. 소문자 정규화.
    3. 별칭 딕셔너리에서 조회.

    Args:
        name_or_header: 변수명 또는 헤더 문자열.
        lookup: 커스텀 {소문자별칭→표준명} 딕셔너리 (None이면 기본 전역 딕셔너리 사용).

    Returns:
        CF 표준명 문자열, 매칭 없으면 ``None``.
    """
    if lookup is None:
        lookup = _LOOKUP
    cleaned = _UNIT_BRACKET.sub("", name_or_header).strip()
    return lookup.get(cleaned.lower())
