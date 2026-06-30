# 실데이터가 드러낸 스킬 요구사항 (M1–M4 구현자 전달용)

- 작성: A팀 / Youjung Oh (오유정) — 데모 시나리오(`DEMO_SCENARIO.md`) 작성 중 실데이터 점검에서 발굴.
- 대상: `validate-model-output` M1–M4 구현(최범규).
- 요지: 통합설계(`...unified-design.md`)는 **정규 1D/2D 격자 + 영문/UTF-8**을 전제했는데, 실제 파랑 검증 데이터(WW3 mesh + 한글 cp949 부이)가 그 전제를 벗어난다. 데모 A(파랑)가 깨지지 않으려면 아래가 필요하다. **우선순위·해당 마일스톤** 표기.

> 점검 환경: `.venv`(py3.9) + xarray, 실파일 `project/data/`. 재현 명령은 각 항목에 첨부.

---

## 0.5 M1 실측 검증 결과 (TC-A1 `discover` 대조 — 예측이 증거로 확인됨)

`python scripts/cli.py discover project/data` 실행 결과:
- ✅ **기상쌍 정상**: ERA5→`meteorology`/reference/1d, GFS→`meteorology`/output/2d (TC-B 통과).
- ❌ **R1 확인**: 부이 CSV **30개 전부 `(열기 실패: 미지포맷)`** — utf-8 디코딩 실패. (크래시는 없음 = no-crash 설계 정상)
- ⚠️ **R2 확인 + 신규**: WW3 5개가 `coord_kind=1d`로 **오판**(실제 mesh), 도메인 **`meteorology`로 오분류**, role=unknown.
  - **신규 발견(R2b/R4)**: WW3가 `uwnd/vwnd`(eastward/northward_wind)를 포함 → router 투표 **기상 2 > 파랑 1(`hs`)**. 도메인 판정이 풍성분에 끌려감.
  - 또 `변수` 칼럼에 `longitude,latitude,tri,MAPSTA`(좌표·격자 정의)가 데이터변수로 노출 → 표시·판정에서 좌표/보조변수 제외 필요.

→ 아래 R1·R2는 **예측이 아니라 확인된 결함**. R4에 "대표변수 우선 도메인 판정"을 추가한다.

---

## 0.6 M3+ 검증 결과 (TC-A 재실행 — 대부분 해결, 신규 블로커 1)

M3(+일부 M4) 푸시 후 재검증. 스킬 테스트 **241 passed / 1 failed**.
- ✅ **R1 인코딩 해결**: 부이 cp949 CSV가 **열림**(컬럼 인식). 
- ✅ **R2 해결**: WW3가 `coord_kind=mesh`·domain=`waves`·role=output로 정확 분류.
- ✅ **신규 기능**: `verify` 서브커맨드 + `preprocess`·metrics(basic/pattern/distribution/circular)·`plots`·recipe 문서.
- ⚙️ **R3-b — 점관측 좌표 출처는 "에이전트가 파악"할 것 (코어에 하드코딩 금지)**: 실 부이 CSV(`OBS_BUOY_TIM`)·번들 fixture 모두 **lat/lon 컬럼이 없고**, 좌표는 **`points.list`에 정점ID(`지점`)로 분리**돼 있음. 단, `points.list`는 **자료마다 형식·이름·유무가 다르므로 코어에 박으면 안 됨**(하드코딩 금지 원칙). verify의 "실데이터 헤더 확인하고 적응하라" 메시지가 **설계대로의 신호**.
  - **에이전트(SKILL.md PHASE1)**: "점관측에 좌표 없음 → 폴더에서 좌표 출처(별도 points/메타 파일) 탐색하거나 사용자에 질문 → 형식 실시간 파악해 조인" 단계 명문화.
  - **코어(preprocess)**: `points.list` 전용 파서가 아니라 **범용 좌표 주입구**(`{정점ID:(lat,lon)}` 매핑/`--points`는 형식불문, 에이전트가 파싱해 전달). 코어는 "좌표 주어지면 mesh 최근접 매칭"만 책임.
- ⚠️ **R4 잔여**: 부이 도메인이 `meteorology`로 잡힘(부이에 풍속·기압·기온 등 기상컬럼이 파랑컬럼보다 많아 투표 우세). 파랑 매칭 의도와 어긋날 수 있음 → **유의파고(headline) 가중** 또는 사용자 확정으로 보완.
- ⚠️ **GFS 회귀 의심**: GFS `coord_kind`가 이전 `2d`→현재 `none`. mesh 리팩터 영향 가능 → 2D 좌표(lat/lon as 2D data_vars) 인식 점검 필요.
- ⚠️ **단위테스트 1건 실패**: `test_metrics_circular::test_constant_array_nan`(상수배열 원형상관 NaN 처리).

→ **요지**: R1·R2는 끝. 파랑 데모는 **에이전트가 좌표 출처를 파악·조인**(R3-b, 코어엔 범용 주입구만)하면 완성 — points.list 하드코딩 금지. GFS 회귀·circular 테스트는 사소하나 기록.

---

## R1. CSV 인코딩 자동감지 + 한글 헤더 매핑 〔치명적 · M1(io_detect)+M3(aliases)〕

**증상(재현됨):** 부이 CSV는 **cp949**, 컬럼이 **한글**(`유의파고(m)`·`파주기(sec)`·`파향(deg)`·`수온(°C)`·`풍속(m/s)`…).
```
pd.read_csv("OBS_BUOY_TIM_2024.csv")            # → UnicodeDecodeError (utf-8) ✗
pd.read_csv(..., encoding="cp949")              # → OK ✓
```
**현 설계 결함:** `io_detect.open_dataset`의 `pd.read_csv`(utf-8 기본)가 **즉시 예외**. `router/domains.yaml`은 영문 standard_name·패턴 기반이라 한글 부이는 **도메인 미탐지**.
**필요 변경:**
1. `io_detect`: CSV 읽기 시 인코딩 **순차 시도**(utf-8 → cp949 → euc-kr → latin-1) 또는 감지. 실패해도 크래시 금지(unknown).
2. `config/aliases.yaml`에 **한글 변수 별칭** 추가:
   - `유의파고`→`Hs`(significant_wave_height), `최대파고`→Hmax, `평균파고`→Hmean
   - `파주기`→`Tm`(period), `파향`→`dir`(wave_to_direction), `수온`→SST(sea_water_temperature), `풍속/풍향`→wind, `기온/기압/습도`
   - 단위 괄호 표기(`(m)`,`(sec)`,`(°C)`) 파싱.
3. `router`: alias 적용 후 도메인 판정(한글→표준명 변환 후 매칭). `유의파고/파주기/파향` → **waves**.
4. 시간 컬럼 `일시`(`YYYY-MM-DD HH:MM`) → 표준 time 파싱, 지점 컬럼 `지점`(station id)을 좌표축으로.

## R2. 비정형 격자(unstructured mesh) 인식 〔높음 · M1(dataset)+M3(preprocess)〕

**증상:** WW3는 정규 lat/lon 격자가 **아님** — `node` 차원(287,759) 기반, `longitude(node)`·`latitude(node)`가 1D 데이터변수, 삼각망 `tri(element,3)`.
```
xr.open_dataset("geo_ww3_anal_20240916.nc").sizes
# {'node':287759,'time':24,'element':574253,'noel':3}  ← lat/lon 격자축 없음
```
**현 설계 결함:** `Dataset.coord_kind()`가 `'1d'|'2d'|'none'`만 반환 → mesh를 `none`으로 보거나 grid_shape 오판. `regions`(bbox crop)·`preprocess`(격자정렬)가 정규격자 가정.
**필요 변경:**
1. `dataset.py`: `coord_kind`에 **`'mesh'`** 추가 — `lon/lat`이 동일한 단일 차원(`node`)을 공유하고 격자축이 없으면 mesh로 판정. `latlon()`이 node 기반 1D 좌표를 반환.
2. `discover/inspect`: mesh도 크래시 없이 인벤토리(노드 수·시간·변수 요약).
3. `regions.py`: mesh는 bbox를 **node 마스크**로 crop(격자 슬라이싱 불가).

## R3. 모델(격자/mesh) ↔ 점관측(CSV) matchup/colocation 〔높음 · M3/M4(preprocess/verify)〕

**상황:** 파랑 검증 = WW3(mesh) 값을 **부이 점좌표**(`points.list` 17점 / 부이 CSV 31점)에서 뽑아 비교. 격자대격자가 아니라 **mesh→점 최근접**.
**필요 변경:**
1. `preprocess`: **점 매칭 경로** — 부이 (lon,lat)마다 WW3 node 중 **최근접(KDTree/BallTree, 가능하면 haversine)** 1개(또는 k-NN 평균) 추출. 거리 임계 초과 시 제외+경고.
2. 시간 정합: 둘 다 hourly → 공통 시각 교집합으로 paired sample.
3. 결과 구조: `{station, time, model_val, obs_val}` 롱포맷 → metrics 입력.
4. (선택) `points.list`(공백구분 `lon lat 'id'`) 파서.

## R4. 변수 별칭 — 모델/관측/재분석 3원 매핑 〔중간 · M3(aliases)〕

같은 물리량이 자료원마다 이름이 다름 → `aliases.yaml`에 통합:
| 표준 | WW3(모델) | 부이(관측) | ERA5(재분석) |
|---|---|---|---|
| 유의파고 Hs | `hs` | `유의파고(m)` | `swh`(있으면) |
| 파주기 | `t01`/`fp` | `파주기(sec)` | `mwp` |
| 파향 | `dir`/`dp` | `파향(deg)` | `mwd` |
| 수온 SST | — | `수온(°C)` | `sst` |
| 바람 | `uwnd/vwnd` | `풍속/풍향` | `u10/v10` |

> 주의(검증 함정): **파주기 정의 불일치** — WW3 `t01`(평균주기)와 부이 `파주기`(첨두/영점교차 여부 불명)는 정의가 다를 수 있음 → 리포트에 정의 명시·동일정의 비교 권고(§G).

**추가(R4b) — 도메인 판정 보강 (M1 검증서 확인):**
- **대표변수 우선**: 다수결 대신, 도메인 고유 "headline" 변수에 가중. WW3는 `hs`(파랑) 존재 시 풍성분(`uwnd/vwnd`)보다 **파랑 우선** (현재 기상으로 오분류됨).
- **좌표·보조변수 제외**: `longitude/latitude/tri/MAPSTA/depth` 등은 도메인 투표·변수표시에서 제외(데이터변수로 새는 문제 확인됨).
- **role 힌트 보강**: 파일명 `anal`(분석/모델 산출)도 output 후보 힌트로 추가(현재 WW3 role=unknown).

## R5. (마이너) WW3 상태맵·partition 〔낮음 · M2/M4〕
- `MAPSTA`(status map: 해양/육지/비활성 node) → 비활성 node 마스킹(가짜 결측 방지).
- partition(`phs0/1/2`,`pdir0/1/2`,`pws*`) = windsea/swell 분리 → 고급 recipe(reference-only)로 연결.

---

## 마일스톤 매핑 요약
| 요구 | 우선 | 모듈/파일 | 마일스톤 |
|---|---|---|---|
| R1 인코딩+한글alias | 치명 | io_detect, aliases.yaml, router | M1·M3 |
| R2 mesh 인식 | 높음 | dataset.coord_kind, regions | M1·M3 |
| R3 점 matchup | 높음 | preprocess, verify | M3·M4 |
| R4 3원 변수별칭 | 중 | aliases.yaml | M3 |
| R5 MAPSTA/partition | 낮 | qc, recipes | M2·M4 |

**한 줄 결론:** 데모 A(파랑)를 살리려면 **R1(한글 cp949)·R2(mesh)·R3(점 matchup)** 3개가 필수. 셋 다 통합설계의 모듈 경계 안에서 확장 가능(새 모듈 불필요) — `io_detect`/`dataset`/`preprocess`에 분기 추가 + `aliases.yaml` 데이터로 흡수.
