from dataset import Variable
from rules import load_rules, match_rule


def _var(name, units=None, standard_name=None):
    return Variable(name=name, dims=("y", "x"), shape=(2, 2),
                    units=units, standard_name=standard_name, long_name=None, attrs={})


def test_load_rules_structure():
    r = load_rules()
    assert "rules" in r and "default" in r
    assert isinstance(r["rules"], list) and len(r["rules"]) >= 1


def test_match_temperature_kelvin():
    rule = match_rule(_var("t2m", units="K", standard_name="air_temperature"))
    assert rule is not None
    assert rule["valid_min"] <= 200 and rule["valid_max"] >= 320  # K 범위


def test_match_temperature_celsius_distinct_from_kelvin():
    # 같은 이름(tmp)이라도 단위가 degC면 K 규칙이 아니라 C 규칙에 매칭
    rule = match_rule(_var("TMP", units="degC"))
    assert rule is not None
    assert rule["valid_min"] < 0 and rule["valid_max"] < 100  # C 범위 (음수 허용)


def test_match_pressure_pa():
    rule = match_rule(_var("PRMSL", units="Pa", standard_name="air_pressure_at_mean_sea_level"))
    assert rule is not None
    assert rule["valid_max"] > 50000  # Pa


def test_no_match_returns_none():
    assert match_rule(_var("mystery", units="widgets")) is None
