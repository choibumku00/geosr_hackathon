# 스킬 검증 시나리오 (Acceptance Test) — `validate-model-output`

- 작성: A팀 / Youjung Oh (오유정)
- **목적: 스킬이 완성되면 이 시나리오로 "제대로 동작하는가"를 검증한다.** 실데이터(WW3 파랑모델 vs 부이 관측, GFS vs ERA5)를 입력으로, 각 단계마다 **기대결과 + PASS 판정기준**을 미리 못박아 둔 **인수테스트(acceptance test)**다. (발표 데모는 이 검증을 그대로 시연하는 것 → §부록)
- 검증 대상 = 4페이즈(`discover→elicit→verify→report`) + 다축 배터리 + §G 함정 강제.
- 데이터가 드러낸 선행 요구사항 → `SKILL_REQUIREMENTS_FROM_DATA.md` (이게 충족돼야 아래 TC가 통과).
- 보안: 실제 지점좌표·실측 raw는 본 문서에 넣지 않음(일반화). 원본·`points.list`는 로컬 `project/data/`(git 제외). 수치는 "관찰 예시"이며 실행 결과로 대조.

---

## 0. 검증 입력 인벤토리 (테스트 픽스처)

| 파일(일반화) | 역할 | 도메인 | 포맷 | 격자 | 시기 |
|---|---|---|---|---|---|
| `geo_ww3_anal_2024091{4..8}.nc` | 모델 | 파랑 | NetCDF4 | **비정형 mesh**(node ~287k) | 2024-09-14~18 시간별 |
| `OBS_BUOY_TIM_2024.csv` | 관측(기준) | 파랑(+기상) | **CSV/cp949/한글헤더** | 점(한국근해 ~31지점) | 2024 시간별 |
| `points.list` | 검증 지점좌표 | — | ASCII | 점 17 | — |
| `gfs_fcst_glo_day_masked_20220906.nc` | 모델 | 기상 | NetCDF4 | 2D 격자 | 2022-09-06 |
| `era5_rean_glo_day_20220906.nc` | 기준(재분석) | 기상 | NetCDF3 | 1D 격자 | 2022-09-06 |
| `(생성) ww3_broken.nc / buoy_broken.csv` | 고의결함 | — | — | — | QC 적발 검증용 |

> WW3 변수: `hs`(Hs)·`t01`(주기)·`dir`(파향)·`fp`·`uwnd/vwnd`·partition. 부이 컬럼: `유의파고(m)`·`파주기(sec)`·`파향(deg)`·`수온(°C)`·`풍속/풍향`·…

---

## 1. 검증 스위트 A — 파랑(WW3 vs 부이) 〔주〕

### TC-A1 · PHASE0 discover (멀티포맷·멀티도메인 발견)
- **입력/실행:** `python scripts/cli.py discover project/data/`
- **기대결과:** 인벤토리 표 + `inventory.json`. WW3=`waves`/`mesh`/role=output, 부이 CSV=`waves`/point/role=reference, GFS·ERA5=`meteorology`.
- **PASS 판정:**
  - [ ] 5종 파일이 모두 행으로 나오고 크래시 없음
  - [ ] WW3 `format=netcdf4`, `coord_kind=mesh`(또는 node 표기)
  - [ ] 부이 CSV가 `format=csv`로 **열림**(cp949) 且 `domain=waves`로 탐지
  - [ ] GFS=netcdf4·meteorology, ERA5=netcdf3·meteorology, 좌표 2d/1d 구분

### TC-A2 · PHASE1 elicit (질문 유도)
- **입력:** (애매) "이 모델 결과랑 관측 검증해줘"
- **기대결과(에이전트가 되물어야 함):** ① 모델=WW3 / 기준=부이 확인 ② 도메인 파랑 확인 ③ 변수=Hs·주기·파향 ④ 기간=겹치는 09-14~18 ⑤ 해역별? ⑥ (갭) "위성 고도계 있으면 triple collocation 가능" 안내.
- **PASS 판정:**
  - [ ] **즉시 분석 시작하지 않고** 역할·도메인·변수·기간을 질문으로 확정
  - [ ] 질문이 `recipes.yaml` 파랑 항목 기반(임의 생성 아님)
  - [ ] 미보유(위성)는 "가능 분석"으로만 안내

### TC-A3 · PHASE2 preprocess (인코딩·alias·mesh→점 매칭)
- **실행:** `verify`의 전처리 단계
- **기대결과:** cp949 디코딩 + 한글컬럼 alias(유의파고→Hs 등) + 부이점→WW3 **최근접 node**(KDTree) + hourly 시간 교집합 → paired sample(`station,time,model,obs`).
- **PASS 판정:**
  - [ ] 부이 CSV 한글헤더가 표준변수로 매핑됨
  - [ ] 각 부이점에 매칭된 node·거리(임계 초과 제외) 로그
  - [ ] paired 표본 수 > 0, 시간축 정렬됨

### TC-A4 · PHASE2 다축 배터리 (단일지표 금지 검증)
- **기대결과(축마다 산출):**

| 축 | 산출 | metrics | 그림(카탈로그) | PASS 체크 |
|---|---|---|---|---|
| 정확도 | Hs bias·RMSE·**SI**·r·기울기 | basic | 산점도+SI(`18`) | [ ] 수치+그림 |
| 분포 | Hs QQ·PDF·분위수 | distribution | QQ(`18`/`16`A) | [ ] 꼬리 비교 |
| 시간 | 지점 시계열+잔차·lag | timeseries | overlay(`18`) | [ ] 피크 가시화 |
| 방향 | 파향 원형 평균오차·원형상관 | circular | wave rose(`18`) | [ ] ±180° 처리 |
| 이벤트 | 09-15 피크 적중·임계초과 | events | 피크·return(`16`C) | [ ] peak/timing |
| 종합 | Taylor/target(지점·변수) | pattern | Taylor(`16`A) | [ ] 다지점 요약 |
| 해역 | 동/남/서해 crop 반복 | regions | 해역별 표 | [ ] mesh crop |

- **관찰 예시(실행 후 실값 대조):** 09-15경 부이 Hs **~6 m** vs WW3 **~4.6 m** → "이벤트 시 첨두 과소모의" 가설을 SI·피크·QQ꼬리로 정량화(단정 아님, 결과로 판정).
- **PASS 판정:** [ ] **최소 3축(정확도+분포/패턴+편향)** 동시 산출, [ ] 각 축 그림 생성.

### TC-A5 · PHASE3 report (§G 함정 강제)
- **기대결과:** `report.md`(요약→정확도표→분포→시계열→방향→그림→가정/advisory/미수행) + `report.json`.
- **PASS 판정:**
  - [ ] 캡션/문장에 "부이=점관측(대표성오차), WW3−부이 **차이**(모델 '오차' 단정 금지)", "SI<0.15 등 **advisory**", "단일지표 결론 금지" 자동 포함
  - [ ] 각 수치에 **근거**(지점·해역·값)
  - [ ] 같은 입력 재실행 → **같은 결론**(재현성)

---

## 2. 검증 스위트 B — 기상(GFS vs ERA5) 〔보조: 범용성·QC〕

### TC-B1 · QC 결함적발 (검증 자동화의 핵심)
- **실행:** `validate <ERA5 정상 clip>` / `validate <고의결함본>`(기온 500K·결측구멍·격자 비단조·잘림)
- **PASS 판정:** [ ] 정상=전 체크 PASS, [ ] 결함본=해당 체크마다 **FAIL+근거**(예: "t2m 12값>340K @idx…", "lat 비단조 @i=…"), [ ] 크래시 0.

### TC-B2 · 격자대격자 verify (단위·좌표 정렬)
- **실행:** `verify <GFS> --ref <ERA5>`
- **PASS 판정:** [ ] °C↔K 정규화, [ ] 2D↔1D 좌표 정렬, [ ] 기온·바람 bias/RMSE·Taylor·차이지도·풍향 원형통계·해역별 산출.
- **메시지(검증 포인트):** 포맷·규약(°C/K·2D/1D·mesh/격자·영문/한글)을 **안 가리는 범용성** 입증.

---

## 3. 검증 통과 마스터 매트릭스 (완성 후 체크)
- [ ] TC-A1 discover 멀티포맷/도메인 분류
- [ ] TC-A2 elicit 질문유도(즉시분석 금지)
- [ ] TC-A3 cp949+한글alias+mesh→점 매칭
- [ ] TC-A4 파랑 다축(≥3축)+그림
- [ ] TC-A5 report §G 경고+재현성
- [ ] TC-B1 QC 정상PASS/결함FAIL
- [ ] TC-B2 GFS↔ERA5 단위·좌표 verify
- [ ] (선행) `SKILL_REQUIREMENTS_FROM_DATA.md` R1·R2·R3 충족

> 하나라도 FAIL → 해당 모듈/요구사항으로 피드백(R1~R5). 이 매트릭스가 "스킬이 동작한다"의 객관 근거(②재현성).

---

## 부록 — 발표 시연 매핑 (검증을 그대로 보여줌)
- **60초 미니시연 = TC-A1 + TC-A4 + TC-A5**: `discover`(멀티포맷 자동분류) → 파랑 `verify`(Hs 산점도+SI·09-15 피크 시계열·파향 rose) → 리포트 §G 경고 자동출력.
- **QC 임팩트 = TC-B1**: 정상 통과 / 결함 정확 적발 한 화면.
- 5분 흐름: (30s)문제 →(60s)해법(4페이즈+카탈로그) →(120s)라이브 A+B →(60s)재현·전파(yaml만 수정) →(30s)Before/After+한계.
- 1인 60초 분담(③전원참여): discover+QC / 파랑 다축 verify / 해역·이벤트.
- 리스크: 사전녹화 `submit/evidence/`, 오프라인 소형 clip, 미완분은 "가능 분석"으로 표기.
