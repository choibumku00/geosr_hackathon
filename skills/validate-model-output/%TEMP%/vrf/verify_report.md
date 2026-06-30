# Verify 리포트 — 격자↔격자

- **모델**: `clean_era5_like.nc`
- **기준**: `clean_era5_like.nc`
- **정보**: 공통 변수 3개: ['t2m', 'u10', 'v10']

## § 정확도 (Accuracy)

| 변수 | N | Bias | RMSE | SI | Pearson r |
|---|---|---|---|---|---|
| t2m | 108 | 0.0000 | 0.0000 | 0.0000 | - |
| u10 | 108 | 0.0000 | 0.0000 | 0.0000 | - |
| v10 | 108 | 0.0000 | 0.0000 | 0.0000 | - |

## § 분포 (Distribution)

Q-Q Plot: ![QQ Plot](C:\Users\choir\OneDrive\文件\지오시스템리서치\geosr-hackathon-kit\skills\validate-model-output\%TEMP%\vrf\qq_t2m.png)

## § 시간 (Time)

Scatter: ![Scatter](C:\Users\choir\OneDrive\文件\지오시스템리서치\geosr-hackathon-kit\skills\validate-model-output\%TEMP%\vrf\scatter_t2m.png)
Timeseries: (없음)

## § 방향 (Direction)

(방향 변수 없음 — 파향·풍향 변수를 확인하라)

## § 종합 (Summary)

Taylor Diagram: ![Taylor](C:\Users\choir\OneDrive\文件\지오시스템리서치\geosr-hackathon-kit\skills\validate-model-output\%TEMP%\vrf\taylor_t2m.png)
Diff Map: (없음)

> **[§G Advisory]** 기준자료(reference)는 truth가 아닙니다. 단일 지표·단일 그림만으로 모델 성능을 결론짓지 마십시오. 임계 판정 없음(advisory) — 도메인·변수·해상도별 합격 기준을 별도 정의하십시오. 이상치·기기 오류·시공간 매칭 오차를 실데이터에서 반드시 점검하십시오.
