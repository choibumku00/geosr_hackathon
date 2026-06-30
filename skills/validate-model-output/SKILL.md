---
name: validate-model-output
description: 수치모델/AI 출력을 NetCDF/CSV로 받아 발견→질문유도→다축 검증·분석한다. 사용자가 데이터/요구를 명확히 말하지 않으면 먼저 discover로 무엇이 있는지 파악하고 되묻는다.
---

# validate-model-output

수치모델 출력을 ERA5/GLORYS·관측·위성과 비교·검증하는 범용 스킬. **분석을 즉시 시작하지 않는다.** 먼저 무엇이 어디에 어떤 형태로 있는지 발견하고, 모르는 것은 사용자에게 질문해 구체화한다.

## PHASE 0 — DISCOVER (분석 전 필수)
1. 작업폴더/지정경로를 인벤토리한다:
   `python scripts/cli.py discover <폴더 또는 파일...>`
   → 파일별 포맷·도메인·좌표·역할추정 표 + `inventory.json`.
2. 단일 파일 구조가 궁금하면:
   `python scripts/cli.py inspect <파일>`
3. **미지/예상 밖 포맷**(`openable=false`, `unknown=true`)이면: 표시된 `head_hex`·확장자를 단서로 **즉석 점검 코드를 작성**해 구조를 파악한 뒤, 발견 내용을 사용자에게 보고하고 reader 확장 여부를 결정한다.

## PHASE 1 — ELICIT (질문으로 구체화)
인벤토리를 사용자에게 제시하고 되묻는다:
- 어느 파일이 '우리 결과물'이고 어느 것이 '기준/검증'인가? (역할추정은 파일명 휴리스틱일 뿐 — 확인받는다)
- 도메인이 확정되면, 그 도메인에 유용한 기준자료(재분석 격자·관측 CSV·위성)가 있으면 어떤 분석이 가능한지 안내하고 보유 여부를 묻는다.
- 애매하지만 가치 있는 분석은 옵션으로 제시하고 고르게 한다.

## PHASE 2 / 3 — VALIDATE·VERIFY·REPORT
(후속 마일스톤 M2~M5에서 구현: `validate`(QC) / `verify`(다축 배터리) / `report`)

> 원칙: 기준자료는 truth가 아니라 reference. 해석 임계는 advisory. 단일 지표/그림으로 결론내지 않는다.
