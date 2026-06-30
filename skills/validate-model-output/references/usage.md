# 사용법 (재현 가이드)

## 설치
```
# 실행 위치: skills/validate-model-output/
python -m pip install -r requirements.txt
python scripts/make_fixtures.py        # 기상 합성 fixture 생성 (테스트용)
python scripts/make_waves_fixtures.py  # 파랑 합성 fixture 생성 (WW3 mesh + 부이 cp949)
python -m pytest -v                    # 전체 테스트 (421 passed / 0 warnings)
python scripts/run_acceptance.py       # 인수테스트 5/5 PASS 확인
```

## PHASE 0 — 발견 (discover / inspect)
```
python scripts/cli.py discover .          # 현재 폴더 인벤토리
python scripts/cli.py discover ../../project/sample_data
python scripts/cli.py inspect path/to/file.nc
```
- 출력: 파일별 포맷(netcdf3/netcdf4/csv/unknown)·도메인 추정·좌표(1d/2d/mesh)·역할추정(output/reference) + `inventory.json`.
- 미지 포맷은 `openable=false`, `unknown=true`로 표시되고 `head_hex`가 함께 나온다.
- `--out` 옵션으로 inventory.json 저장 경로 지정 가능.

```
python scripts/cli.py discover path/to/data --out /tmp/inv.json
python scripts/cli.py inspect path/to/ww3_mesh.nc   # mesh coord_kind 확인
```

## PHASE 1 — 층위1 QC (validate)

```
python scripts/cli.py validate path/to/model.nc
python scripts/cli.py validate path/to/model.nc --out /path/to/out_dir/
```

- 출력: stdout 에 Markdown 리포트 + `out_dir/qc_report.json`, `out_dir/qc_report.md` 저장.
- `config/rules.yaml` 의 변수 범위·결측률·단위 규칙을 적용한다.
- PASS / FAIL / WARN 세 단계로 반환. `ok=false` 이면 exit code 1.
- `config/rules.yaml` 에 없는 변수는 N-sigma 이상치 탐지만 적용(WARN).

**QC 규칙 추가 예:**
```yaml
# config/rules.yaml 에 추가
- name: custom_wave_period
  match_name: ["tp_obs", "t01", "tm01"]
  valid_min: 1.0
  valid_max: 30.0
  units_any: "s"
  max_missing_frac: 0.1
```

## PHASE 2 — 다축 검증 (verify)

### 기본 구문

```
python scripts/cli.py verify MODEL_FILE --ref REF_FILE [옵션]
```

| 옵션 | 설명 |
|------|------|
| `--ref FILE` | 기준(재분석/관측) 파일 경로 (필수) |
| `--out DIR` | 리포트·그림 저장 폴더 (기본: 현재 폴더) |
| `--points FILE` | 관측점 목록 파일 (lon lat id 형식; 점관측 CSV 에 좌표 없을 때) |
| `--regions 이름,…` | 해역별 분석 해역 쉼표 목록 (예: `동해,남해,서해`) |
| `--model-tz TZ` | 모델 시간대 (UTC \| KST \| +09:00; 기본=UTC 가정) |
| `--ref-tz TZ` | 기준 파일 시간대 (부이 KST vs 모델 UTC 면 9h 어긋남 주의) |

### 격자대격자 (GFS↔ERA5, 기상 도메인 예)

```
python scripts/cli.py verify gfs_output.nc \
  --ref era5_ref.nc \
  --out ./verify_out/ \
  --regions 동해,남해
```

- 동일 격자(coord_kind=1d/2d) 판정 → `_verify_grid_to_grid()` 자동 선택.
- 공통 변수명 교집합으로 정확도(bias/RMSE/SI/r) 계산.
- 방향 변수(`dir`, `wdir`, `dp`, …) 감지 → 원형 통계(circular_cme/rmse/corr) 추가.
- 온도 변수(`t2m`, `sst`, …) 단위 불일치(K↔°C) 자동 정규화.
- 그림 출력: `scatter_<var>.png` · `taylor_<var>.png` · `qq_<var>.png` · `diff_map_<var>.png` · `rose_model_<var>.png`.
- `--regions` 지정 시 해역 bbox 마스크 적용해 해역별 표 추가.

### mesh + 점관측 (WW3↔부이, 파랑 도메인 예)

```
python scripts/cli.py verify ww3_mesh.nc \
  --ref buoy_obs.csv \
  --out ./verify_out/ \
  --ref-tz KST \
  --points stations/points.list \
  --regions 동해,남해
```

- mesh coord_kind 감지 → `_verify_mesh_point()` 자동 선택.
- `match_points_to_mesh(max_km=50)` 최근접 노드 매칭.
- `--ref-tz KST` → `tz_to_utc` 로 -9h 적용 후 `common_time_index` 교집합.
- TZ 미지정 → "UTC 가정, KST면 9h 어긋남" 경고를 리포트에 삽입.
- 그림 출력: `scatter_<var>.png` · `qq_<var>.png` · `timeseries_<var>.png` · `taylor_<var>.png` · `diff_map_<var>.png` · `rose_model_<var>.png`.

### verify 출력 파일

```
verify_out/
  verify_report.json   # 메트릭·매칭 정보 (모드/ok/accuracy_rows/direction_rows/plots/regions)
  verify_report.md     # Markdown 리포트 (§G 캡션 포함)
  scatter_hs.png
  qq_hs.png
  taylor_hs.png
  timeseries_hs.png
  diff_map_hs.png
  rose_model_dir.png
  rose_ref_dir.png
```

## 시간대(TZ) 처리 상세

관측(부이 등)과 모델의 시간축 TZ 가 다르면 매칭에서 최대 9h 오차가 생긴다.

**확인 순서:**
1. NetCDF — `d.xr["time"].attrs.get("units", "")` 로 CF units 확인.
2. CSV — 보통 TZ 표기 없음. 컬럼 값에 "+09:00" 포함 시 KST; 없으면 사용자에게 질문.
3. 부이: KST(UTC+9) 흔함. 수치모델: 보통 UTC.

```python
from preprocess import tz_to_utc
times_utc, assumed = tz_to_utc(times, tz="KST")
# assumed=True 이면 리포트 경고: "TZ 미확인=UTC가정; KST면 9h 어긋남 위험"
```

`tz_to_utc` 지원 값: `'UTC'` · `'KST'` · `'+09:00'` · `'+0900'` · `None`(UTC 가정).

## 점관측 좌표 주입 (`--points`)

점관측 CSV 에 lat/lon 컬럼이 없을 때 외부 좌표 파일로 주입한다.

**points.list 형식** (공백/탭 구분, `#` 주석):
```
# lon  lat  station_id
129.04 35.12 STN001
126.93 33.46 STN002
```

**CLI 사용:**
```
python scripts/cli.py verify ww3_mesh.nc --ref buoy.csv \
  --points stations/points.list --ref-tz KST
```

**Python API:**
```python
from preprocess import inject_point_coords, parse_points_list

mapping = parse_points_list("stations/points.list")  # {id: (lat, lon)}
lats, lons = inject_point_coords(df["station"].values, mapping)
# lats, lons → cKDTree 매칭에 사용
```

주의: `parse_points_list` 는 에이전트/CLI 명시 호출 전용.
코어 자동 경로에 삽입하지 말 것.

## 미지 포맷 대응

```
python scripts/cli.py inspect unknown_file.bin
```
→ `openable=false` + `head_hex` 출력 → 에이전트가 throwaway 파서 작성.

## 적응 가이드 참조

실데이터 적응(mesh 구조 확인·cp949 CSV·TZ·점관측 좌표·throwaway 코드 원칙)은
`references/adapting.md` 참조.
