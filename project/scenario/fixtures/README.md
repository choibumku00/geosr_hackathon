# 데모/인수테스트 fixture — 정답지 (Expected QC Findings)

`make_demo_fixtures.py`가 생성하는 정상본 + 고의결함본. **TC-B1(QC 결함적발)** 검증·발표 데모용.
- ERA5(공개 재분석)는 실파일을 작게 잘라 사용(`project/data/era5_rean_glo_day_20220906.nc` 필요).
- 부이는 민감자료라 **합성**(cp949·한글헤더) — 실측치 아님(지점 `DEMO01`).
- 재현: `python make_demo_fixtures.py`

## 파일별 주입 결함 ↔ 스킬이 잡아내야 할 것 (정답지)

| 파일 | 주입한 결함 | 기대 QC 결과 |
|---|---|---|
| `era5_demo_clean.nc` | (없음) | **PASS** — 전 체크 통과 |
| `era5_demo_broken.nc` | t2m 9칸=**500K**, t2m 150칸 **NaN**, u10 1칸=**999**, lat 좌표 2점 **swap(비단조)** | **FAIL** — value_range(t2m·u10) FAIL, grid_monotonic FAIL, outlier WARN |
| `era5_demo_truncated.nc` | 정상본을 **60%만 남겨 손상** | **FAIL(open)** — 크래시 없이 열기 실패 보고 |
| `buoy_demo_clean.csv` | (없음, cp949·한글헤더) | 열림(R1 후) → PASS |
| `buoy_demo_broken.csv` | 유의파고 **99.9**·**-1.0**, 파주기 4칸 결측, 파향 **999**, 시간 중복·깨진 타임스탬프 | 열림(R1 후) → value_range·missing·time FAIL |

> 부이 CSV는 현재(M2) **cp949 미지원이라 열기 실패** — 요구사항 R1 충족 시 위 결함을 적발해야 한다(인수 기준).

## 실측 검증 결과 (M2 스킬 대조, 2026-06-30)

`python scripts/cli.py validate <fixture>` 실행:
- `era5_demo_clean.nc` → **PASS (12/12)** ✅
- `era5_demo_broken.nc` → **FAIL** — t2m value_range(500K 9개)·u10 value_range(999)·grid_monotonic 비단조 적발, outlier WARN ✅
- `era5_demo_truncated.nc` → **FAIL(open)** 무크래시 ✅
- `buoy_demo_broken.csv` → **FAIL(open)** utf-8 디코딩 실패 → **R1 미구현 확인** ⚠️

발견된 보강점: ① 국소 결측(0.78%)이 60% 임계 미만이라 미적발 → 연속결측 체크 고려 ② 손상본 에러 메시지 개선(현재 'h5py 없음'으로 표시) ③ R1(cp949)은 M3 예정.

## 보안
실측 부이값·지점좌표는 본 폴더·문서에 없음(합성). 대용량 원본은 `project/data/`(git 제외).
