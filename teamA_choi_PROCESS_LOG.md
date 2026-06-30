# PROCESS_LOG — 작업 기록 (과정 70점의 핵심 근거)

> 표준 헤더(CLAUDE.md 등)를 로드했다면 에이전트가 알아서 채워 줍니다. 비면 직접 채우세요.
> 원칙: **실제로 시킨 프롬프트를 그대로 인용**할 것. 요약만 있으면 점수가 깎입니다.

## 작성자 정보 (개인별 로그 — 본인 것만)
- 팀명: A
- 본인 이름(작성자): 최범규
- 공통과제(우리 팀이 자동화한 반복 수작업): 모델 후처리 및 검증 자동화
- 내가 맡은 부분: 모델 검증 분석 범용 Skill 설계·논문조사·구현 (도메인 자동판별 + 비교/통계/시각화 + 리포트 자동화)
- 자유과제(있으면):

> **이 로그는 본인 것만 작성**합니다. 각자 자기 PC·계정으로 작업해 개인 로그를 남기고, 제출 시 **영문 파일명** `<팀영문명>_<이름로마자>_PROCESS_LOG.md`(예: `teamA_kim_PROCESS_LOG.md`)로 저장하세요. **한글 파일명은 압축 시 깨지므로 금지** — 한글 팀명·이름은 위 '작성자 정보'에 적습니다. 운영자가 팀별로 모아 채점합니다(전원 참여 = 팀별 개인 로그 수).

## 효과 측정 (Before → After, 결과 ⑥ 채점용 — 형식 자유)
> **지표는 자기 업무에 맞게 고름 — 강제 항목 없음.** (예시, 해당되는 것만) 소요 시간 · 반복 횟수 · 다루는 자료/파일 수 · 손 가는 단계 수 · 품질·일관성 · 오류/누락 · 커버리지 등. 정량이 어려우면 정성도 인정.

| 지표(자기 업무에 맞게) | Before(기존 수작업) | After(에이전트화) |
|------|------|------|
| 재현율(같은 입력→같은 결론) | ≈0% (즉석 4구현 PASS/FAIL 1:3 불일치) | 100% (validate 3회 report SHA-256 동일) |
| 결함 탐지·점검 일관성 | 구현마다 다른 항목→결함 통째 놓침 | rules.yaml 전항목 고정 점검(누락 0) |
| 지원 포맷·도메인 | 담당자마다 별도(비정형 mesh·한글 cp949 미지원) | NetCDF3/4·CSV(cp949/euc-kr)·mesh + 도메인 자동판별 |
| 분석 깊이 | 단일 지표(RMSE) 즉석 | 다축(정확도+분포+시간+방향+종합+해역)+§G 함정 강제 |
| 규모·품질 | 검증 없음 | 모듈 19+테스트 34파일 421 passed/0 warnings, 인수 5/5 |
| 전파성 | 개인 스크립트·머릿속 | Claude Code 스킬 등록(yaml 확장)+97KB 배포 zip |

> 상세 실측·근거: `submit/BEFORE_AFTER.md` + `project/scenario/consistency_experiment/RESULT.md`.

## 사용 기법 (권장·가점, 필수 아님)
- [x] (a) 서브에이전트 / 역할 분담  — 문헌조사를 31개 서브에이전트 Workflow로 분담(도메인/방법군별 1에이전트, 2단계 파이프라인)
- [x] (b) 외부 도구·데이터 연동 (파일/API/MCP/사내데이터)  — WebSearch/WebFetch로 논문 1차 출처 실재 검증
- [x] (c) 재사용 산출물 (스킬 / 프롬프트셋 / CLAUDE.md / 서브에이전트 구성)  — 분석 검증 범용 Skill의 references/recipes 토대(`project/research/` 카탈로그 + `REVIEW.md`)와 재사용 Workflow 산출물 생성

---

## 작업 로그 (단계마다 1개씩 누적 / 시간순)

### [#1] 파랑 도메인 검증 방법 카탈로그 보강·출처 검증
- 작성자(팀원): 최범규
- 목표: Skill의 references/recipes 토대인 `project/research/08_domain_waves.md`(파랑 도메인)에 빠진 정통(canonical) 검증법을 추가하고, 인용 출처를 웹으로 실제 확인해 지어낸/의심 인용을 정정·'확인요' 표기.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "위 파일을 Read로 읽고, (1) 빠진 핵심/정통(canonical) 방법을 추가하고, (2) 출처가 실제로 존재하는지 웹으로 점검해 의심스러운/지어낸 인용을 제거하거나 '확인요'로 표기하고, (3) 메서드 카드 형식·해석기준을 더 충실히 다듬어 같은 경로에 Write로 덮어써라."
- 사용한 기법(있으면): (b) WebSearch로 12편 이상 논문 인용 1차 검증
- 결과: 메서드 카드 22 → 27개로 확장(추가: OLS 기울기·절편 회귀 / 스펙트럼 모멘트 mₙ 비교 / 범주형 임계초과 POD·FAR·CSI / 확률예보 CRPS·Brier·ROC / ERA5 격자-격자 공간비교). 인용 정정: 1997 ECMWF 검증 논문 1저자를 'Bidlot'→'Janssen, Hansen & Bidlot'로, Bowers et al.(2000) 제목을 실제 *Applied Ocean Research* "Directional statistics of the wind and waves"로 수정, HY-2B 논문 출판연도 2024→2025 정정, Caires&Sterl/McColl/Jolliff/Hersbach/Mentaschi 등은 권·페이지·DOI 확인해 병기. 확인 실패한 'Bidlot & Holt(2006 JCOMM)'는 제거하고 ECMWF Newsletter No.150으로 대체, '확인요' 섹션 신설. GLORYS가 파랑변수를 직접 제공하지 않는다는 점을 명시(대조군은 ERA5/WAVERYS).
- 막힘 → 해결: HY-2B 논문 DOI(rs17233829)가 파일엔 2024로 적혀 있었으나 검색 결과 MDPI Remote Sensing vol17/issue23/2025로 확인 → 연도 정정하고 DOI는 유지.

### [#2] 수온·염분 도메인 검증 방법 카탈로그 보강·출처 검증
- 작성자(팀원): 최범규
- 목표: Skill의 references/recipes 토대인 `project/research/09_domain_ocean_temp_salinity.md`(수온·염분 도메인)에 빠진 정통(canonical) 검증법을 추가하고, 인용 출처를 웹으로 실제 확인해 의심/지어낸 인용을 정정하거나 '확인요'로 표기. 특히 "우리 모델 vs ERA5/GLORYS/관측/위성, NetCDF격자+CSV시계열" 비교에 실제로 쓸 방법 우선 보강.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "위 파일을 Read로 읽고, (1) 빠진 핵심/정통(canonical) 방법을 추가하고, (2) 출처가 실제로 존재하는지 웹으로 점검해 의심스러운/지어낸 인용을 제거하거나 '확인요'로 표기하고, (3) 메서드 카드 형식·해석기준을 더 충실히 다듬어 같은 경로에 Write로 덮어써라."
- 사용한 기법(있으면): (b) WebSearch/WebFetch로 1차 문헌 서지정보·URL 실재 검증(약 9건)
- 결과: 메서드 카드 24 → 28개로 확장(추가: ① Target diagram(Jolliff et al. 2009) — bias vs 비편향 RMSD 분해 시각화, ② GODAE Class-4 관측공간 검증(Ryan et al. 2015) — 모델을 관측위치로 보간해 SST/SLA/수직T/수직S를 공정 비교하는 운영 표준틀, ③ Spiciness/spice(Flament 2002; McDougall & Krzysik 2015) — 등밀도면 수괴 추적자, ④ 강건 오차통계(median bias/MAD/robust RMSE)). 출처 정정: de Boyer Montégut(2004 MLD)·Holte & Talley(2009 MLD 알고리즘) "확인요" 해제하고 DOI 확정(10.1029/2004JC002378, 10.1175/2009JTECHO543.1); 장벽층(BLT) 출처를 막연한 "확인요"에서 de Boyer Montégut et al.(2007, JGR, doi:10.1029/2006JC003953)로 명시; 불안정한 ResearchGate 자동생성 figure URL(D20)을 NOAA PMEL TAO·IRI/LDEO 정식 출처로 교체; de Souza et al.(2020 NZ)·Verezemskaya et al.(2021)·Ryan et al.(2015) 저자 전체 보완; Taylor TSS 식을 Taylor(2001) 식 4 정규화형 `S=4(1+r)/[(σ̂+1/σ̂)²(1+r₀)]`로 정정. 모든 1차 문헌에 DOI 병기.
- 막힘 → 해결: 파일이 BLT를 "de Boyer Montégut et al. BLT 연구(표준 참고문헌, 확인요)"로만 적어 정확한 서지가 없었음 → 검색으로 BLT 전구 기후값의 정통 출처가 de Boyer Montégut et al.(2007) JGR "Control of salinity on the mixed layer depth in the world ocean: 1"임을 확인해 DOI와 함께 확정.

### [#3] 검증·분석 방법 문헌 카탈로그 — 31개 서브에이전트 Workflow로 광범위 수집·정리
- 작성자(팀원): 최범규
- 목표: 만들 Skill의 references/recipes 토대로, 해양·기상 수치모델 "검증·분석 방법"을 가능한 한 망라해 `project/research/`에 도메인/방법군별 md로 정리. (모델↔모델·관측·위성 비교, 영역 crop, 에너지·흐름 보존, RMSE 등 통계, AI 분석까지 포함)
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "기존 논문들을 탐색해서 어떤 분석들을 하는지 찾아봐줘. 수치모델이랑 수치모델을 비교할 수 있고 관측 자료랑 비교할 수도 있고, 광범위한 영역이면 특정 영역을 crop해서 분석할 수도 있잖아. 에너지들이 보존되는지, rmse는 어떤지 흐름이 잘보존 되는지 등등 다양한 분석들이 있을거야. ... 스킬을 범용적으로 분석에 사용 할 수 있되, 특정 도메인에 특화가 가능하도록 해줘. 일단 기존 논문들의 분석 방법들을 최대한 많이 수집 하고, md파일에 정리해줘. 파일은 너무 길어질것 같으면 너가 잘 분할해서 적어줘."
  > (오케스트레이션 지시) "도메인/방법군별로 에이전트를 나눠 각자 웹조사 → 해당 md 작성 → 출처 검증·보강(2단계 파이프라인), 마지막에 색인·분류체계·누락점검 에이전트가 README와 분류체계를 정리"
- 사용한 기법: (a) 서브에이전트 31개 분담(Workflow, 2단계 파이프라인) + (b) WebSearch/WebFetch 출처 검증
- 결과: 15개 카탈로그 파일(01~15) + 색인 2종 생성, **방법카드 약 500개**(파일당 17~65개), 총 ~870KB.
  - 분석유형: 01 오차통계 / 02 공간패턴 / 03 범주·확률·극값 / 04 보존·에너지·플럭스 / 05 스펙트럼·EOF·모달 / 06 시계열·신호
  - 도메인: 07 기상 / 08 파랑 / 09 수온·염분 / 10 해류·조류 / 11 해수면·조위
  - 자료원·틀: 12 위성 / 13 모델상호비교·앙상블 / 14 AI·ML 평가 / 15 전처리·격자정합
  - 색인: `00_overview_taxonomy.md`(11범주 트리 + 4축 라우팅 + **도메인→레시피 매핑** + 횡단 정규화표 + Skill 구현 지침), `README.md`(목적·파일목록·사용법·Gaps)
  - 통계: 에이전트 31개 / 도구호출 534회 / 처리시간 ~27분 / 서브에이전트 토큰 ~272만
- 막힘 → 해결: 03·09 파일이 메서드 카드를 `###` 대신 `##`로 작성(형식만 상이, 내용 정상) — 후속 정규화 대상으로 기록. 출처는 enrich 단계에서 웹 교차검증해 지어낸 인용 제거/'확인요' 표기(상세는 #1·#2 참조).

### [#4] Research 카탈로그 품질 검토·구현 적합성 분석
- 작성자(팀원): 최범규
- 목표: `project/research/`에 생성된 검증·분석 방법 카탈로그가 우리가 만들 "모델 후처리 및 검증 자동화 Skill"의 토대로 적합한지 전체적으로 점검하고, 잘된 점·보완점·다음 구현 우선순위를 정리.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "우리가 하려는것을 제대로 이해해야해. 일단 너가 전체적으로 research 된 것을 확인하고 분석해서 잘됐는지 내용은 괜찮은지 확인해줘."
- 사용한 기법(있으면): (b) 로컬 파일 검사·검색(`rg`, UTF-8 샘플링) / (c) 재사용 산출물 `project/research/REVIEW.md` 작성
- 결과: 카탈로그가 Skill 설계 토대로 충분하다고 판정. `00_overview_taxonomy.md`의 도메인 자동판별→recipe 매핑, `15_preprocessing_regridding_colocation.md`의 전처리 게이트, `01` 기본통계, `08` 파랑, `09` 수온·염분, `12` 위성, `14` AI/ML 평가가 핵심 자산임을 확인. 보완점으로 ① 카드 형식 정규화(`03`·`09` heading, `06`·`12` 라벨), ② 임계값을 advisory로 분리, ③ 중복 지표 canonical 구현화, ④ MVP 범위 축소 필요를 정리. 상세 검토 결과를 `project/research/REVIEW.md`에 저장.
- 막힘 → 해결: PowerShell 기본 출력 인코딩에서 한글이 깨져 보였으나 `Get-Content -Encoding utf8`로 재확인해 파일 자체는 정상 UTF-8임을 확인.

### [#5] REVIEW.md 검토의견 수용 → 카탈로그 형식 정규화·안전원칙 명문화
- 작성자(팀원): 최범규
- 목표: `REVIEW.md`(검토자 Codex)의 지적 중 "지금 카탈로그에 반영할 것"을 수용해 내용 개선. 코드/스펙 사안(canonical 모듈·MVP 범위·`project/spec/*`)은 다음 단계로 분류.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "REVIEW.md 여기에 검토 내용이 있는데, 읽어보고 수용할 내용 수용해서 내용 개선해줘."
- 사용한 기법(있으면): (b) Python(UTF-8) 스크립트로 형식 정규화 일괄 적용·검증
- 결과:
  - **(4.1 형식 정규화)** 메서드 카드 형식 통일 → 자동 파싱(카드→함수 stub) 대비. `03`·`09`: 메서드 헤딩 `##`→`###` 승격(각 37·29개, 목차·출처 섹션은 `##` 유지). `06`·`12`: 카드 7라벨 굵게(`- 무엇을 측정:`→`- **무엇을 측정**:`, 각 182·147개). 목차 불릿·본문은 불변 — 과잉적용 0 검증.
  - **(6.3 함정 명문화 + 4.3 임계값)** `00_overview_taxonomy.md`에 "**§G 검증 해석의 함정 — 반드시 지킬 원칙**" 신설: ① 기준자료≠참값(reference) ② 오차 독립성 점검 ③ 동화·보간 산물 독립관측 취급 금지 ④ 해석 임계값 advisory(영역·해상도 의존 경고) ⑤ '확인요' 출처 확정인용 금지 ⑥ 단일 지표 금지(정확도+편향+패턴+유의성). `README.md` 상단에 ⚠️ 포인터 추가.
  - **(다음 단계로 분류)** 4.2 위성 canonical 함수 승격 / 4.4 canonical metric 모듈 / 4.5 MVP 범위 축소 / 6.1 `project/spec/*` 산출물 → 스펙·구현 단계에서 수용 예정(REVIEW 스스로 "다음 단계 권장"으로 분류).
- 막힘 → 해결: 헤딩 일괄 변환 시 목차·출처 섹션까지 `###`로 바뀔 위험 → 제외어(목차/출처/References/Methods Index) 필터 + 라벨 굵기 정규식에 길이·접두어 제한을 둬 색인 불릿 오변환 방지, grep으로 사후 검증.

### [#6] 팀원 설계 스펙 통합 검토 및 최적화안 도출
- 작성자(팀원): 최범규
- 목표: git pull 이후 들어온 팀원 설계(`docs/superpowers/specs/2026-06-30-validate-model-output-design.md`)를 읽고, 기존 research 카탈로그와 결합해 구현 가능한 최적 설계 방향을 구체화.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "git pull하고 push도 했는데 팀원이 작업 한 내용이 왔을거야. 읽어보고 설계 최적화 및 구체화 해줘."
- 사용한 기법(있으면): (b) git 상태/최근 커밋/스펙 파일/카탈로그 파일 로컬 분석
- 결과: 팀원 스펙의 강점은 `결정적 Python 코어 + rules.yaml + QC/예보검증 데모`이고, research의 강점은 `도메인 router + recipes + canonical metric 근거`임을 확인. 최적 설계는 둘을 합친 hybrid로 제안: `rules.yaml`은 단일파일 QC, `recipes.yaml`은 기준자료 비교/도메인별 분석으로 분리하고, MVP는 NetCDF/CSV 중심의 QC + 같은격자 비교 + markdown report로 제한. GRIB native reader와 일반 regrid는 후속으로 분리.
- 막힘 → 해결: 팀원 스펙에 "GRIB 자동 감지/처리"와 "GRIB 네이티브 reader는 범위 밖"이 동시에 존재 → MVP에서는 GRIB 원본 직접처리를 제외하고, 변환된 NetCDF 또는 메타데이터 alias 처리만 지원하는 것으로 설계 경계 정리.

### [#7] 통합 설계 스펙 확정·작성·커밋 (발견·유도 + 다축 배터리)
- 작성자(팀원): 최범규
- 목표: 팀원 스펙 + research 카탈로그 + REVIEW를 단일 구현 가능 설계로 통합하고, "바로 분석"이 아니라 보유 데이터·검증셋을 먼저 파악·질문으로 유도한 뒤 research 기반 다방면 분석을 돌리는 스킬로 설계를 구체화·최적화.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "현재 프로젝트 내용을 이해하고 흐름을 잡아줘. 그리고 다음으로 무엇을 할지 말해줘. 설계를 좀 더 구체화 및 최적화 하는 방향으로."
  > "분석을 바로 시작하는게 아니라 현재 결과물을 확인할 수 있으면 어떤 형태로 어떻게 저장돼있는지 확인하고 검증 및 비교할 데이터는 어떤 것으로할지 … 물어봐 … 예상치 못한 파일 형태가 들어오면 그에 맞는 형태로 코드를 실시간으로 작성하여 파일 형태를 파악해 … 질문은 애매하게 시작할 수 있어도 계속 질문을 해서 답을 유도하고 분석을 구체적으로 해주는 skill이 되도록 해줘."
  > "분석을 다방면으로 해줘야해. 간단한 rmse 분석만 해주면 안되고 … 특정 해역만 crop해서 수온 형태를 본다던가 … 아까 사전 리서치 한내용을 잘 활용해 … 최대한 다양한 분석을 해줘야해."
- 사용한 기법(있으면): (b) 로컬 환경·데이터 점검(Python 모듈·pip 설치가능 여부·NetCDF 시그니처·파일크기 확인) / (c) brainstorming 스킬로 설계 수렴 후 재사용 산출물 스펙 작성
- 결과: `docs/superpowers/specs/2026-06-30-validate-model-output-unified-design.md` 작성·커밋(cca3f8c). 핵심 결정: ① 4-페이즈 흐름(discover→elicit→validate/verify→report, 분석 즉시 시작 금지·질문 유도) ② 미지 포맷 실시간 점검·1..N 기준자료·reference-type 적응 ③ research 카탈로그 기반 다축 분석 배터리(정확도·패턴·분포·시간·벡터·물리·해역 crop) + feasibility 자동판정 ④ `rules.yaml`⟂`recipes.yaml` 직교 + `metrics/` canonical 단일구현 ⑤ advisory 임계·reference(≠truth). 환경 확인: Python3.12+numpy/pandas/matplotlib/scipy 보유, `xarray netCDF4 h5netcdf PyYAML pytest` 설치가능. 데이터: ERA5=NetCDF3(598MB)/GFS=NetCDF4·HDF5(1.14GB), 둘 다 전역 721×1440·단일일.
- 막힘 → 해결: 사용자가 "시간·팀원 스펙을 제약으로 깔지 말고 프로젝트 품질 우선"으로 방향 재지정 → 초기의 시간박스 최소 MVP안을 버리고, 라우터·전처리·canonical metric을 실제 범용으로 설계하되 500개 전부 구현은 YAGNI로 배제(라이브=기상, 타 도메인=recipe 정의만).

### [#8] git pull·머지·push + 팀원 figures 시각화 카탈로그를 스펙에 반영
- 작성자(팀원): 최범규
- 목표: 팀 저장소(myrepo)에서 pull해 충돌 해결·push하고, 새로 들어온 팀원의 검증 시각화(그림) 레퍼런스 카탈로그(`project/research/figures/16~22`)를 통합 설계 스펙의 다축 배터리·리포트에 시각화 매핑으로 반영.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "github에서 pull 해주고 충돌있으면 해결해주고, push까지 해줘."
  > "1번으로 진행해줘" (= 방금 들어온 figures 카탈로그를 스펙 §7/§10에 반영 후 구현 계획으로 진행)
- 사용한 기법(있으면): (b) git 도구연동(fetch/merge/push, 충돌 사전분석) / (c) 팀원 재사용 산출물(figures 카탈로그)을 설계에 결합
- 결과: fetch로 팀원 커밋 `6a8bd7f`(figures 16~22 + README, 그림카드 ~115개) 확인 → 변경파일이 내 스펙과 겹침 0 확인 → `ort` 자동머지(충돌 없음, 머지커밋 `9bd3d56`) → push 성공, `main`이 `myrepo/main`과 동기화. 이어 통합 스펙(`...unified-design.md`)에 figures 반영(커밋 `1d454a5`): §7 다축 배터리 표에 '그림' 열 추가(축→figure 카드 매핑), `plots.py` 모듈 신설(각 그림의 "만드는 법" 실존 Python 도구 구현), §10 리포트에 축별 figure 임베드 + 캡션에 §G 3원칙(reference≠truth·advisory·단일그림 금지) 강제, §13 `cartopy` optional(미설치 시 pcolormesh 대체).
- 막힘 → 해결: 분기(local=스펙커밋 / remote=figures커밋)였으나 `git diff --stat`으로 변경파일 비교해 디렉토리가 완전 분리됨을 미리 확인 → 충돌 없이 머지 진행.

### [#9] 구현 계획(M1 기반·발견) 작성 — TDD 8태스크
- 작성자(팀원): 최범규
- 목표: 통합 스펙을 마일스톤(M1~M5)으로 분할하고, 첫 마일스톤 M1(Dataset 추상화·포맷감지·router·inspect·discover + CLI)을 단계별 TDD 구현 플랜으로 작성.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "정식 스펙 문서로 작성·커밋하고 구현 계획으로 넘어가줘." → writing-plans 스킬로 M1 플랜 작성.
- 사용한 기법(있으면): (c) writing-plans 스킬로 재사용 가능한 구현 플랜(테스트·코드·커밋 단위까지 명시) 산출
- 결과: `docs/superpowers/plans/2026-06-30-validate-model-output-m1-foundation.md`(커밋 `ba7a8bf`). 8태스크: ①스캐폴드·의존성 ②Dataset/Variable 추상화 ③합성 fixture(NetCDF3+NetCDF4) ④io_detect 포맷감지·라우팅 ⑤router 도메인판별+domains.yaml ⑥inspect_file 프로브(미지포맷 no-crash) ⑦discover 인벤토리+cli ⑧SKILL.md PHASE0/1 골격+usage. 합성 fixture로 hermetic 테스트(원본 1.14GB 비의존, 전파성↑), 미지포맷은 크래시 대신 unknown 플래그. M2~M5는 후속 별도 플랜(플랜 말미에 예고). self-review로 스펙 커버리지·타입 일관성 확인(예: 표준 `inspect` 충돌 회피 위해 모듈명 `inspect_file.py`).
- 막힘 → 해결: 스펙이 한 스킬이지만 컴포넌트가 많고 verify/metrics가 "실제 GFS 변수명·단위"에 의존(스펙 §13서 추정) → 단일 거대 플랜 대신 마일스톤 분할, M1의 discover가 실데이터 구조를 확정해 후속 추정 제거하도록 설계.

### [#10] M1(기반·발견) 서브에이전트 주도 구현 — 8태스크 TDD + 2단계 리뷰 + 최종 브랜치 리뷰
- 작성자(팀원): 최범규
- 목표: M1 플랜을 서브에이전트 주도(subagent-driven-development)로 실제 구현 — 태스크마다 구현 서브에이전트 → spec+품질 리뷰 서브에이전트 → fix 루프, 마지막에 전체 브랜치 리뷰 후 main 머지.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "서브에이전트로 주도해줘." / "1번으로 해주고 그다음 작업을 추천해줘"(= feature 브랜치로 구현 후 main 머지)
- 사용한 기법: (a) 서브에이전트 역할분담 — 태스크별 구현(sonnet)/리뷰(sonnet)/최종리뷰(opus) 분리, 진행원장(.superpowers/sdd/progress.md)로 상태추적 (c) 재사용 자산 — 동작하는 스킬 `skills/validate-model-output/` 산출
- 결과: feature 브랜치에 10커밋, **테스트 26 passed/0 warnings**, main 머지(`884a492`)·push. 모듈: dataset.py(포맷무관 Dataset+open_nc), io_detect.py, router.py+domains.yaml, inspect_file.py(no-crash 프로브), discover.py+cli.py, 합성 fixture(NetCDF3/4), SKILL.md(PHASE0/1), usage.md. 리뷰에서 잡아 고친 핵심: ① conftest 전역 몽키패치→`dataset.open_nc` 공유 헬퍼로 이전(한글경로 production 대응) ② requirements에 scipy/h5py 추가(한글경로 NetCDF3 유일 엔진) ③ probe no-crash 구멍 봉합(디렉터리/못읽는 파일 구조화 반환) ④ pytest.ini로 출력 pristine. **실데이터 스모크로 설계 추정 확정**: GFS=2D곡선격자·8시각·TMP/DPT(℃)/UGRD/VGRD/PRATE/PRMSL(Pa), 도메인신뢰도 0.211(낮음). 부이 CSV 존재(open 실패).
- 막힘 → 해결: 리포지토리 경로의 한글(지오시스템리서치)로 netCDF4 C 라이브러리가 OSError(Errno22) — 처음엔 conftest 몽키패치로 우회했으나 리뷰가 "production 경로 미보호"를 지적 → fallback을 `dataset.open_nc`(엔진 default→h5netcdf→scipy)로 옮겨 io_detect가 재사용하게 구조화, scipy를 의존성에 명시해 신규 설치에서도 동작 보장.

### [#11] M2(QC/validate) 서브에이전트 주도 구현 — 6태스크 + 최종 브랜치 리뷰(fill-value 발견)
- 작성자(팀원): 최범규
- 목표: 기준자료 없이 파일 하나를 물리·형식 상식으로 점검하는 층위1 QC(`validate`) 구현 — 단위인식 규칙·값범위·결측·이상치·격자·시간축 검사 → PASS/FAIL/WARN 리포트(json+md).
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "1번으로 진행해줘"(= M2 플랜 작성 → 서브에이전트로 실행)
- 사용한 기법: (a) 서브에이전트 6태스크 구현/리뷰 분리(sonnet) + 최종 브랜치 리뷰(opus), 진행원장 추적 (c) 재사용 자산 — `config/rules.yaml`(코드 무수정 확장점)·qc/report 모듈
- 결과: feature 브랜치 8커밋, **54 tests green**, main 머지(`3c7d833`)·push. `rules.yaml`(단위별 규칙: temperature_K/_C·wind·mslp_Pa·precip·salinity)+`rules.py`(K vs degC 단위인식 매칭), `qc.py`(check_variable/grid/time/schema + run_qc), `report.py`(json+md, advisory·reference≠truth 명문), `cli validate`(clean→exit0/broken→exit1), 고의결함 fixture(정상PASS/결함FAIL 자동보증), domains.yaml GFS 패턴 보강.
- 막힘 → 해결: **GFS 실데이터 스모크에서 6개 변수 value_range FAIL이 전부 마스킹 안 된 GRIB 기본 _FillValue(9.969e36=NC_FILL_DOUBLE) 탓**임을 발견(실제 위반 아님) → 최종 리뷰 판단으로 `check_variable`에 센티넬 가드(`|v|≥1e30`→결측 분류) 추가해 즉시 신뢰성 확보(intrinsic QC로 타당, 환산 아님). 또 이모지(✅❌⚠️)가 한글 Windows 콘솔(cp949)에서 UnicodeEncodeError로 헤드라인 명령을 크래시시키는 것을 리뷰가 적발 → cli 진입에서 stdout utf-8 재설정으로 no-crash 보장.

### [#12] 병렬 멀티에이전트 워크플로로 파랑 언블록+적응형 샘플 일괄 구축 (방식 전환)
- 작성자(팀원): 최범규
- 목표: 단계별 순차 리뷰가 느려서 **속도를 위해 병렬 팬아웃(Workflow)**으로 전환하고, 철학도 "모든 걸 구현"이 아니라 **"파이썬은 대략적 구조파악용 샘플/템플릿, 실전에선 에이전트가 실시간 구조점검·도메인 맞춤 코드를 작성"**으로 재정의. 팀원(오유정) 실데이터 요구(R1 cp949·R2 mesh·R4b 도메인)를 한 번에 언블록.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "최대한 많은 Task를 병렬로 만들고 똑똑한 AI들이 병합을 해주는 식으로 하자. 단계단계만드니까 너무 오래걸려."
  > "지금 파이썬 코드는 파일을 대략적으로 구조를 파악하는 용도고 … 실전에서 안돌아간다면 그때 즉각적으로 구조 파악 코드 같은걸 만들고 실시간으로 파악 … 개인화/도메인 특화된 코드를 작성해서 분석"
  > "좀더 병렬에이전트로 많은 task를 한번에 돌려줬으면 해"
- 사용한 기법: (a) **Workflow 멀티에이전트 오케스트레이션 — 한 팬아웃에 13개 에이전트 동시 + 통합·opus리뷰**(파일 소유 분리로 충돌 0, 통합 에이전트가 병합) (b) 외부 데이터 규약(cp949/mesh) 흡수 (c) 재사용 산출물 대량 생성
- 결과: feature 브랜치 1커밋(병렬 산출 일괄), main 머지(`6db1011`)·push. **242 tests / 0 warnings**. 산출: core(io_detect cp949 폴백·dataset mesh `coord_kind='mesh'`·router R4b 파랑 headline 우선·discover 'anal' role) + 적응형 SAMPLE 모듈(metrics_basic/circular/distribution/pattern·plots·preprocess[mesh→점 KDTree matchup·to_kelvin]·aliases[한글헤더 매핑]) + cli `verify`(격자대격자/mesh-점 graceful) + 정상/결함 파랑 fixture + **SKILL.md live-adaptive 두뇌**(실시간 구조점검·도메인 맞춤 코드 작성 지시)·references(adapting·recipe_waves·recipe_meteorology). 스모크: WW3=waves/mesh, 부이 CSV=cp949 열림. 워크플로 통계: 15에이전트/서브토큰 ~68만/처리 ~15분.
- 막힘 → 해결: 처음엔 단계장벽(fixtures→core→build5)로 5병렬뿐 → 사용자가 더 넓게 요구 → 진행 중 워크플로 중지(부분 추적편집 git checkout 리셋, 완성 fixture는 유지) 후 **장벽 제거·플랫 모듈화(metrics_*.py 패키지 대신)**로 13개를 한 팬아웃에 재배치. 남은 갭(부이 CSV가 열리나 domain=unknown — router가 한글 alias 미적용)은 후속(작은 보강)으로 분류.

### [#13] 패키징 직전 종합 마무리 — 버그수정+verify다축+R3b/R4+tz+인수테스트 (14에이전트 병렬)
- 작성자(팀원): 최범규
- 목표: 패키징 전 남은 작업을 한 번에 끝내기. 팀원이 GitHub에 올린 재검증 결과(GFS 2D 회귀·circular 실패·R3-b 좌표·R4 부이도메인)와 재현성 실험을 모두 흡수해, 파랑/기상 verify 다축 배터리를 실배선하고 인수테스트를 자동화.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "지금 해야하는거 전부 리스트해. 산출물 자료가 KST인지 UTC인지도 잘확인해야해. 모르면 사용자에게 질문하고. 모든 작업을 다 적용해서 병렬 워크 플로우를 해줘. … 깃허브에 있는것도 pull해서 검증한 결과가 있을거야. 그것도 작업에 추가해서 전부 한번에."
- 사용한 기법: (a) Workflow 14에이전트 병렬(Build 11 동시 → Wire → Integrate → opus Review) (b) GitHub pull로 팀원 검증결과 흡수 (c) 대량 재사용 산출물
- 결과: feature 브랜치 1커밋, main 머지(`f969090`)·push. **421 tests / 0 warnings, 인수테스트 5/5 PASS**. 처리: ①GFS 2D 좌표 회귀 수정(coord_kind 2d 복구, mesh/1D 공존) ②circular 상수배열 NaN ③io 손상 메시지 ④router R4(부이→waves: alias-aware+유의파고 headline) ⑤preprocess tz_to_utc(파라미터화)·inject_point_coords(범용 좌표주입)·parse_points_list(CLI 전용, 코어 하드코딩 금지)·common_time_index ⑥regions(해역 crop)·derive(풍속)·plots+(qq/taylor/rose/diff) ⑦cli verify 다축 실배선(격자대격자 단위정규화+bias/RMSE/SI/Taylor/diff; mesh-점 matchup+QQ/시계열/파향)·report verify 렌더+그림+§G/TZ 경고 ⑧run_acceptance 자동러너(DEMO_SCENARIO TC) ⑨SKILL.md에 TZ확인·점관측 좌표출처 명문화 ⑩submit/BEFORE_AFTER를 재현성 실험으로 채움.
- 막힘 → 해결: 시간대(KST/UTC)는 데모 실파일이 로컬에 없어 확정 불가 → 사용자에 질문(AskUserQuestion) → "모름→스킬이 파악/질문" 선택 → tz_to_utc(times,tz=None)로 **파라미터화**(None=UTC가정+경고)하고 SKILL.md가 use-time에 메타데이터 확인/사용자 질문(부이 KST vs 모델 UTC면 9h 어긋남 경고)하도록 설계. 회귀(GFS 2D)는 mesh 리팩터가 latlon을 coords 한정한 부작용 → 2D를 coords·data_var 모두에서 찾도록 복구하되 mesh와 구분.

### [#14] 시스템 설계 문서(architecture.md) 신규 작성 + usage.md verify/tz/points 섹션 보강
- 작성자(팀원): 최범규
- 목표: 스킬의 설계 철학·데이터 흐름·모듈 책임·확장점을 한 문서에 정리한 `references/architecture.md` 신규 작성, 기존 `references/usage.md`에 verify 서브커맨드·시간대(TZ)·점관측 좌표 주입(--points) 사용법 보강.
- 에이전트에게 시킨 것(실제 프롬프트 핵심 인용):
  > "architecture.md: 시스템 설계 문서 — 결정적 코어 vs 에이전트 껍질 분업 / 데이터흐름(입력→io_detect→Dataset 추상화→router 도메인→[QC 층위1 | preprocess→verify 다축] →report) / Dataset 추상화(1D/2D/mesh, open_nc 한글경로) / 도메인 라우팅·alias / preprocess(tz·단위·mesh→점 matchup·좌표주입) / canonical metrics·plots / 적응(live-adaptive) 경계(무엇이 코드, 무엇이 에이전트 실시간) / 확장점(yaml) / 마일스톤(M1 기반·발견 / M2 QC / 파랑·verify 다축) 요약. 다이어그램은 ASCII로. usage.md(기존 보강): 설치 → make_fixtures → pytest/run_acceptance → discover/inspect/validate/verify 각 실제 명령·옵션·출력설명, 미지포맷·mesh·cp949·TZ·점관측 좌표주입(--points) 사용법, references/adapting.md 링크. 기존 내용 유지하며 verify·tz·points 추가."
- 사용한 기법(있으면): (c) 재사용 산출물 — 스킬 재현·적응 가이드 문서 2종
- 결과: `references/architecture.md` 신규 작성(ASCII 데이터 흐름 다이어그램·verify 분기·적응 경계표·확장점·마일스톤 요약 포함). `references/usage.md` 보강(install에 make_waves_fixtures·run_acceptance 추가; discover에 mesh/--out 예시; validate에 QC 출력·rules.yaml 확장; verify 전체 절 신설 — 격자대격자·mesh+점관측·옵션표·출력파일 목록; TZ 처리 상세; --points 파일 형식·CLI·API 예시; 미지포맷 대응; adapting.md 링크).
- 막힌 점 없음.

---

## 마무리 요약 (1~2줄)
- 가장 효과적이었던 에이전트 활용법: **병렬 멀티에이전트 워크플로**(한 팬아웃에 13~14 에이전트, 파일소유 분리로 충돌 0 + 통합·opus 리뷰 에이전트가 병합) + **서브에이전트 주도 TDD**(태스크별 구현/리뷰/fix 루프). 설계는 brainstorming→설계스펙→마일스톤 구현계획으로 단계화하고, 실데이터 스모크로 가정을 실측 확정. 결과적으로 스킬 23개 모듈·34 테스트·**421 passed/0 warnings·인수 5/5·재현성 100%**.
- 다른 팀이 그대로 따라 하려면 필요한 것: `skills/validate-model-output/` 폴더 복사 → `pip install -r requirements.txt` → `python scripts/cli.py discover|validate|verify`. **새 변수·도메인·자료원은 `config/rules.yaml`·`domains.yaml`·`aliases.yaml`만 수정**(코드 무수정)하면 적용되고, `SKILL.md`가 발견→질문 유도→도메인별 적응분석을 지휘하며 실데이터에서 안 맞으면 그 자리서 구조점검·맞춤코드를 작성. 분석 근거는 `project/research/` 카탈로그(~500 방법카드).
