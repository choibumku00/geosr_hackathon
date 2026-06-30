# 사용법 (재현 가이드)

## 설치
```
python -m pip install -r requirements.txt
python scripts/make_fixtures.py   # 합성 fixture 생성 (테스트용)
python -m pytest -v               # 전체 테스트
```

## PHASE 0 — 발견
```
python scripts/cli.py discover .          # 현재 폴더 인벤토리
python scripts/cli.py discover ../../project/sample_data
python scripts/cli.py inspect path/to/file.nc
```
- 출력: 파일별 포맷(netcdf3/netcdf4/csv/unknown)·도메인 추정·좌표(1d/2d)·역할추정(output/reference) + `inventory.json`.
- 미지 포맷은 `openable=false`로 표시되고 `head_hex`가 함께 나온다.
