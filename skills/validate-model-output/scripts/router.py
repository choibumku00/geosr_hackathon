"""도메인·데이터특성 라우터.

설계 원칙 (범용 검증 스킬):
  1차 축은 **데이터 특성**(자료형 data-form + 변수성질 variable-nature)이다 — 이는 분야 무관.
  도메인은 2차 힌트일 뿐이며, 판별 불가여도 절대 멈추지 않는다(characterize 가 항상
  데이터 특성 기반 일반 배터리를 반환). 도메인 우선순위는 config/domains.yaml 의
  `headline`(대표변수) 가중치로 정하며, 특정 도메인을 코드에 하드코딩하지 않는다.

SAMPLE — 실데이터에선 구조를 실시간 점검하고 도메인 맞춤 코드로 적응하라.
데이터특성/변수성질 감지는 휴리스틱이다 — 애매하면 사용자에게 확인한다.
카탈로그 근거: references/research/00_overview_taxonomy.md (A절 4직교축·C절·D절).
"""
from __future__ import annotations

import os
import re

import yaml

from aliases import to_standard
from dataset import Dataset

_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", "domains.yaml"
)

# 도메인 headline(대표변수) 매칭 시 가중치 (일반 매칭=1)
_HEADLINE_WEIGHT = 3

# 투표에서 제외할 좌표·보조 변수 이름(소문자) 및 standard_name
_COORD_EXCLUDE_NAMES: frozenset = frozenset({
    "longitude", "latitude", "lon", "lat", "time",
    "tri", "element", "node", "mapsta", "depth",
})
_COORD_EXCLUDE_SNS: frozenset = frozenset({"longitude", "latitude"})

# --- 데이터 특성 감지용 차원 이름(소문자) ---
_VERTICAL_DIMS: frozenset = frozenset({
    "depth", "deptht", "depthu", "depthv", "lev", "level", "levels",
    "z", "height", "altitude", "plev", "pressure", "sigma",
    "model_level_number", "nz",
})
_ENSEMBLE_DIMS: frozenset = frozenset({
    "member", "members", "ensemble", "ens", "number",
    "realization", "realisation", "nens",
})
_SPECTRUM_DIMS: frozenset = frozenset({
    "freq", "frequency", "frequencies", "wavenumber",
    "direction", "theta", "n_freq", "n_dir",
})

# --- 변수성질 감지용 패턴 ---
_CIRCULAR_NAME = re.compile(r"dir$|direction|파향|풍향|유향|theta")
_VECTOR_NAME = re.compile(
    r"^u(o|10|wnd|grd|as|cur|10m)?$|^v(o|10|wnd|grd|as|cur|10m)?$"
    r"|eastward|northward|zonal|meridional"
)
_HEAVY_TAIL_SN = ("precipitation", "significant_wave_height", "wave_height",
                  "wind_speed", "discharge", "runoff", "surge")
_HEAVY_TAIL_NAME = ("precip", "^hs$", "swh", "hm0", "gust", "discharge", "surge")


def _load_domains(path: str = _CONFIG) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["domains"]


# ---------------------------------------------------------------------------
# 도메인 판별 (2차 힌트 — headline 가중투표, config 주도)
# ---------------------------------------------------------------------------

def _match_var(var, domains: dict):
    """한 변수가 어느 도메인에 맞는지 (headline 무관 일반 매칭).

    우선순위: 1) standard_name 직접 → 2) 변수명 패턴 → 3) alias 표준화 후 재매칭.
    """
    sn = (var.standard_name or "").lower()
    name = var.name.lower()

    for dom, spec in domains.items():
        if sn and sn in [s.lower() for s in spec.get("standard_names", [])]:
            return dom
    for dom, spec in domains.items():
        for pat in spec.get("name_patterns", []):
            if re.search(pat, name):
                return dom
    resolved = to_standard(var.name)
    if resolved:
        resolved_lower = resolved.lower()
        for dom, spec in domains.items():
            if resolved_lower in [s.lower() for s in spec.get("standard_names", [])]:
                return dom
        for dom, spec in domains.items():
            for pat in spec.get("name_patterns", []):
                if re.search(pat, resolved_lower):
                    return dom
    return None


def _classify_var(var, domains: dict):
    """(도메인 or None, is_headline: bool) 반환.

    headline(대표변수)에 먼저 매칭하면 (dom, True) — 가중 3표.
    파랑 등 특정 도메인을 코드에 박지 않고 config `headline` 로 일반화한다.
    """
    sn = (var.standard_name or "").lower()
    name = var.name.lower()
    resolved = to_standard(var.name)
    resolved_l = resolved.lower() if resolved else None

    for dom, spec in domains.items():
        heads = [h.lower() for h in spec.get("headline", [])]
        if not heads:
            continue
        if (sn and sn in heads) or (resolved_l and resolved_l in heads):
            return dom, True
        for pat in spec.get("headline_patterns", []):
            if re.search(pat, name) or (resolved_l and re.search(pat, resolved_l)):
                return dom, True

    return _match_var(var, domains), False


def _is_aux_var(var) -> bool:
    """좌표·보조 변수 여부 — 투표에서 제외."""
    if var.name.lower() in _COORD_EXCLUDE_NAMES:
        return True
    sn = (var.standard_name or "").lower()
    return sn in _COORD_EXCLUDE_SNS


def detect_domain(d: Dataset, domains: dict | None = None) -> dict:
    """도메인 판별 (headline 가중투표). 하위호환 키(domain/confidence/matched) 유지.

    Returns
    -------
    dict: {
        domain     : 최다 가중 도메인 (없으면 'unknown'),
        confidence : 최상위 도메인 가중치 / 전체 가중치 합,
        matched    : {변수명: 도메인},
        candidates : {도메인: 가중치} (내림차순),
        ambiguous  : 상위 2개 가중치가 동률이면 True (→ 사용자 확인 권장),
    }
    """
    if domains is None:
        domains = _load_domains()
    phys_vars = {n: v for n, v in d.variables().items() if not _is_aux_var(v)}

    matched: dict = {}
    weights: dict = {}
    for name, var in phys_vars.items():
        dom, is_head = _classify_var(var, domains)
        if dom is not None:
            matched[name] = dom
            weights[dom] = weights.get(dom, 0) + (_HEADLINE_WEIGHT if is_head else 1)

    if not weights:
        return {"domain": "unknown", "confidence": 0.0, "matched": {},
                "candidates": {}, "ambiguous": False,
                "weak_evidence": True, "unmatched_vars": len(phys_vars)}

    ranked = sorted(weights.items(), key=lambda kv: kv[1], reverse=True)
    best, best_w = ranked[0]
    total_w = sum(weights.values())
    confidence = round(best_w / max(1, total_w), 3)
    ambiguous = len(ranked) >= 2 and ranked[1][1] >= best_w
    # 근거 빈약(weak_evidence): confidence가 높아도 '단정 금지' 신호.
    #   - 물리변수 일부가 어느 도메인에도 안 걸림(정체 불명 변수 존재), 또는
    #   - 단일 비-headline 변수만으로 잡힘(best_w<=1; headline이면 +3이라 제외됨)
    # → SKILL.md 2-A 안전망이 이 플래그에서 사용자 확인을 강제한다.
    #   (headline 매칭이나 다수 변수 합의로 잡힌 경우는 weak 아님 — 정상 기상 파일 오탐 방지)
    unmatched = len(phys_vars) - len(matched)
    weak_evidence = (unmatched > 0) or (best_w <= 1)
    return {"domain": best, "confidence": confidence, "matched": matched,
            "candidates": dict(ranked), "ambiguous": ambiguous,
            "weak_evidence": weak_evidence, "unmatched_vars": unmatched}


# ---------------------------------------------------------------------------
# 데이터 특성 감지 (1차 축 — 분야 무관)
# ---------------------------------------------------------------------------

def detect_data_form(d: Dataset) -> dict:
    """자료형 감지. 분야와 무관하게 파일 구조만으로 판별한다.

    form: grid / mesh / spectrum / profile / point_timeseries / table / unknown
    """
    ck = d.coord_kind()
    dims = {str(x).lower() for x in d.xr.dims}
    has_time = d.time_info() is not None
    has_vertical = bool(dims & _VERTICAL_DIMS)
    has_ensemble = bool(dims & _ENSEMBLE_DIMS)
    has_spectrum = bool(dims & _SPECTRUM_DIMS)

    if ck in ("1d", "2d"):
        form = "grid"
    elif ck == "mesh":
        form = "mesh"
    else:  # 'none' — CSV/점/프로파일/스펙트럼/미지
        if has_spectrum:
            form = "spectrum"
        elif has_vertical and not has_time:
            form = "profile"
        elif getattr(d, "fmt", "") == "csv":
            form = "point_timeseries" if has_time else "table"
        elif has_time:
            form = "point_timeseries"
        else:
            form = "unknown"

    return {"form": form, "coord_kind": ck, "has_time": has_time,
            "has_vertical": has_vertical, "has_ensemble": has_ensemble,
            "has_spectrum": has_spectrum}


def detect_variable_nature(var) -> list:
    """변수성질 태그 감지 (휴리스틱). 검증법이 성질에서 따라 나오게 한다.

    tags: vector / circular / nonnegative / fraction / extreme_prone / continuous
    """
    sn = (var.standard_name or "").lower()
    nm = var.name.lower()
    un = (var.units or "").lower()
    tags: set = set()

    if ("direction" in sn) or _CIRCULAR_NAME.search(nm) or (
        un in ("degree", "degrees", "deg") and ("dir" in nm or "direction" in sn)
    ):
        tags.add("circular")
    if sn.startswith(("eastward_", "northward_", "x_", "y_",
                      "grid_eastward", "grid_northward")) or _VECTOR_NAME.search(nm):
        tags.add("vector")
    if any(h in sn for h in _HEAVY_TAIL_SN) or any(
        re.search(h, nm) for h in _HEAVY_TAIL_NAME
    ):
        tags.add("nonnegative")
        tags.add("extreme_prone")
    if "concentration" in sn or un in ("kg m-2", "mm", "mol m-3", "mg m-3"):
        tags.add("nonnegative")
    if "fraction" in sn or "area_fraction" in sn:
        tags.add("fraction")
        tags.add("nonnegative")
    if not tags:
        tags.add("continuous")
    return sorted(tags)


def characterize(d: Dataset, domains: dict | None = None) -> dict:
    """데이터 특성 우선 종합 프로파일. **절대 막다른 길을 만들지 않는다.**

    도메인이 unknown/애매해도 자료형·변수성질·C-2 트리거로 일반 배터리를 구성해 반환한다.
    카탈로그 근거: references/research/00_overview_taxonomy.md (C-0 공통 / C-2 트리거).
    """
    form = detect_data_form(d)
    natures = {n: detect_variable_nature(v)
               for n, v in d.variables().items() if not _is_aux_var(v)}
    dom = detect_domain(d, domains)

    all_tags = {t for tags in natures.values() for t in tags}
    triggers: list = []
    if form["has_ensemble"]:
        triggers.append("ensemble/probabilistic → rank histogram·CRPS·reliability·spread-skill "
                        "(research 03/13/14)")
    if "circular" in all_tags:
        triggers.append("directional → 원형통계·circular RMSE (research 08/10, figures 18/20)")
    if "vector" in all_tags:
        triggers.append("vector → 복소/벡터 상관·성분(u/v) 오차 (research 10)")
    if "extreme_prone" in all_tags:
        triggers.append("extremes → POT/GPD·GEV·return period (research 03)")
    if form["has_vertical"]:
        triggers.append("profile/section → 깊이별 매치업·단면·T-S (research 09)")
    if form["has_spectrum"]:
        triggers.append("spectral → PSD·파수/방향 스펙트럼 (research 05/08)")

    general_battery = [
        "C-0 공통(항상): 전처리·정합(research 15) → bias/RMSE/SI/r(01) → "
        "Taylor/Target(01) → bootstrap 유의성(01)",
    ]

    if dom["domain"] == "unknown":
        note = ("도메인 미상 — 강제로 도메인을 정하지 말 것. 데이터 특성(자료형+변수성질) "
                "기반 일반 배터리 + 위 트리거로 진행하고, 사용자에게 도메인·역할을 확인하라.")
    elif dom["ambiguous"]:
        note = (f"도메인 후보 복수({', '.join(dom['candidates'])}) — 단정 말고 사용자에게 확인. "
                "확인 전엔 일반 배터리 + 트리거로 진행.")
    elif dom.get("weak_evidence"):
        note = (f"도메인 후보: {dom['domain']} (confidence={dom['confidence']}) — 그러나 근거 빈약"
                "(대표변수 headline 없이 잡혔거나 일부 변수가 미매칭). confidence가 높아도 단정하지 말고, "
                "미매칭·무단위·무표준명 변수의 정체·단위를 사용자에게 확인한 뒤 진행하라.")
    else:
        note = (f"도메인 후보: {dom['domain']} (confidence={dom['confidence']}). "
                "도메인 배터리 + 위 트리거를 적용하되 ELICIT에서 역할을 확인하라.")

    return {"data_form": form, "variable_natures": natures, "domain": dom,
            "triggers": triggers, "general_battery": general_battery, "note": note}
