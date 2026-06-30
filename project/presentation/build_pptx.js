// 발표 PPT 생성 — validate-model-output (수치모델 후처리·검증 자동화)
// 해양 테마. 그림 자리는 점선 빈칸 + 캡션. 한글 폰트: Malgun Gothic.
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
p.author = "A팀 / Youjung Oh";
p.title = "수치모델 후처리·검증 자동화";

const W = 13.33, H = 7.5;
const KF = "Malgun Gothic";
// 팔레트 (Ocean)
const DARK = "11233F", DEEP = "0A5078", TEAL = "1C7293", SKY = "8FC7DE";
const LIGHT = "F4F7FA", INK = "16263B", MUTE = "5B7185", CARD = "FFFFFF";
const PASS = "1E8449", FAIL = "C0392B", AMBER = "E08A1E";

const sh = () => ({ type: "outer", color: "0A1A2E", blur: 9, offset: 3, angle: 135, opacity: 0.16 });

function footer(s, n) {
  s.addText("A팀 · validate-model-output", { x: 0.55, y: 7.05, w: 7, h: 0.3, fontFace: KF, fontSize: 9, color: MUTE });
  s.addText(String(n), { x: 12.4, y: 7.05, w: 0.5, h: 0.3, fontFace: KF, fontSize: 9, color: MUTE, align: "right" });
}

// 콘텐츠 슬라이드 헤더 (밝은 배경 + 제목 + 좌측 작은 사각 모티프)
function header(s, kicker, title) {
  s.background = { color: LIGHT };
  s.addShape(p.shapes.RECTANGLE, { x: 0.55, y: 0.55, w: 0.16, h: 0.55, fill: { color: TEAL } });
  s.addText(kicker.toUpperCase(), { x: 0.85, y: 0.5, w: 11, h: 0.3, fontFace: KF, fontSize: 11, color: TEAL, bold: true, charSpacing: 2 });
  s.addText(title, { x: 0.83, y: 0.78, w: 11.7, h: 0.7, fontFace: KF, fontSize: 27, bold: true, color: INK });
}

// 그림 빈칸 (점선 + 캡션)
function imgBox(s, x, y, w, h, caption) {
  s.addShape(p.shapes.RECTANGLE, { x, y, w, h, fill: { color: "EAF0F5" }, line: { color: TEAL, width: 1.25, dashType: "dash" } });
  s.addText([
    { text: "🖼  그림 삽입", options: { fontFace: KF, fontSize: 13, color: TEAL, bold: true, breakLine: true } },
    { text: caption, options: { fontFace: KF, fontSize: 11, color: MUTE } },
  ], { x: x + 0.1, y: y + h / 2 - 0.45, w: w - 0.2, h: 0.9, align: "center", valign: "middle" });
}

function card(s, x, y, w, h, fill) {
  s.addShape(p.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill || CARD }, rectRadius: 0.08, shadow: sh() });
}

// ───────────────────────── S1 타이틀 ─────────────────────────
{
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addShape(p.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.18, fill: { color: TEAL } });
  s.addShape(p.shapes.OVAL, { x: 10.3, y: -1.6, w: 5.2, h: 5.2, fill: { color: DEEP, transparency: 55 } });
  s.addShape(p.shapes.OVAL, { x: 11.6, y: 3.8, w: 4.2, h: 4.2, fill: { color: TEAL, transparency: 70 } });
  s.addText("공통과제 · 모델 출력 후처리·검증 자동화", { x: 0.9, y: 1.5, w: 11, h: 0.4, fontFace: KF, fontSize: 15, color: SKY, bold: true, charSpacing: 1 });
  s.addText([
    { text: "수치모델 후처리·검증,\n", options: { breakLine: true } },
    { text: "매번 손으로 → ", options: { breakLine: false } },
    { text: "한 번에 일관되게", options: { color: SKY } },
  ], { x: 0.9, y: 2.1, w: 11.3, h: 2.0, fontFace: KF, fontSize: 40, bold: true, color: "FFFFFF", lineSpacingMultiple: 1.05 });
  s.addText("재사용 스킬  ·  validate-model-output", { x: 0.95, y: 4.5, w: 11, h: 0.4, fontFace: KF, fontSize: 16, color: "C7DCEA" });
  s.addText("A팀  ·  발표: 전원 1인 미니시연", { x: 0.95, y: 5.6, w: 11, h: 0.4, fontFace: KF, fontSize: 13, color: MUTE });
}

// ───────────────────────── S2 문제 ─────────────────────────
{
  const s = p.addSlide();
  header(s, "문제 정의", "핵심은 ‘느림’이 아니라 ‘매번 달라짐’");
  const items = [
    ["포맷·규약 제각각", "NetCDF3/4·HDF5·CSV, 좌표 1D/2D/비정형mesh, 단위 K/°C, 영문/한글"],
    ["손으로 오가며 눈으로", "CDO·NCO·Python·ncview·wgrib2를 매번 수동으로 — 느리고 실수"],
    ["세션마다 절차가 달라짐", "쓰는 패키지·기준이 바뀌어 재현 불가, 통과/실패 근거가 안 남음"],
  ];
  let y = 1.9;
  items.forEach((it, i) => {
    card(s, 0.85, y, 11.6, 1.4);
    s.addShape(p.shapes.OVAL, { x: 1.15, y: y + 0.42, w: 0.55, h: 0.55, fill: { color: DEEP } });
    s.addText(String(i + 1), { x: 1.15, y: y + 0.42, w: 0.55, h: 0.55, align: "center", valign: "middle", fontFace: KF, fontSize: 18, bold: true, color: "FFFFFF" });
    s.addText(it[0], { x: 2.0, y: y + 0.22, w: 10.2, h: 0.45, fontFace: KF, fontSize: 18, bold: true, color: INK });
    s.addText(it[1], { x: 2.0, y: y + 0.7, w: 10.2, h: 0.5, fontFace: KF, fontSize: 13, color: MUTE });
    y += 1.6;
  });
  footer(s, 2);
}

// ───────────────────────── S3 통찰 (분업) ─────────────────────────
{
  const s = p.addSlide();
  header(s, "핵심 통찰", "맨손 Claude와 무엇이 다른가 — 역할 분업");
  // 좌: 맨손(약점)
  card(s, 0.85, 1.95, 5.6, 3.4, "FBEDEC");
  s.addText("그냥 에이전트한테 시키면", { x: 1.15, y: 2.2, w: 5.0, h: 0.4, fontFace: KF, fontSize: 16, bold: true, color: FAIL });
  s.addText([
    { text: "매번 코드·패키지·임계가 바뀜", options: { bullet: true, breakLine: true } },
    { text: "검증 항목 누락 가능", options: { bullet: true, breakLine: true } },
    { text: "재현·전파 불가, 근거 안 남음", options: { bullet: true, breakLine: true } },
    { text: "→ ‘껍데기’ 위험", options: { bold: true, color: FAIL } },
  ], { x: 1.2, y: 2.75, w: 5.0, h: 2.4, fontFace: KF, fontSize: 14, color: INK, paraSpaceAfter: 8 });
  // 우: 우리(분업)
  card(s, 6.85, 1.95, 5.6, 3.4, "EAF3EE");
  s.addText("우리 해법 — 결정적 코어 + 에이전트", { x: 7.15, y: 2.2, w: 5.0, h: 0.4, fontFace: KF, fontSize: 16, bold: true, color: PASS });
  s.addText([
    { text: "검증 규칙 → Python·yaml에 박제(완전 재현)", options: { bullet: true, breakLine: true } },
    { text: "판단(모델/기준·분석·해석) → 유도 대화", options: { bullet: true, breakLine: true } },
    { text: "분석 다양성 → 검증 카탈로그(방법500·그림115)", options: { bullet: true, breakLine: true } },
    { text: "→ 일관성 = 맨손이 못 하는 것", options: { bold: true, color: PASS } },
  ], { x: 7.2, y: 2.75, w: 5.0, h: 2.4, fontFace: KF, fontSize: 14, color: INK, paraSpaceAfter: 8 });
  s.addText("대회 최고 배점 ②재현·전파성과 정확히 일치", { x: 0.85, y: 5.7, w: 11.6, h: 0.5, align: "center", fontFace: KF, fontSize: 15, bold: true, color: DEEP });
  footer(s, 3);
}

// ───────────────────────── S4 동작 (4페이즈) ─────────────────────────
{
  const s = p.addSlide();
  header(s, "어떻게 동작하나", "4페이즈 — 분석을 즉시 시작하지 않는다");
  const ph = [
    ["1  발견", "discover", "폴더 스캔 → 포맷·도메인·역할 자동 인벤토리"],
    ["2  질문유도", "elicit", "무엇이 모델/기준인지·변수·기간을 되물어 구체화"],
    ["3  다축검증", "verify", "전처리 정합 → 정확도·분포·방향·시계열 배터리"],
    ["4  리포트", "report", "PASS/FAIL·근거·그림 + §G 경고 자동"],
  ];
  let x = 0.85;
  ph.forEach((c, i) => {
    card(s, x, 2.1, 2.78, 2.7);
    s.addShape(p.shapes.RECTANGLE, { x: x, y: 2.1, w: 2.78, h: 0.5, fill: { color: i % 2 ? TEAL : DEEP } });
    s.addText(c[0], { x: x, y: 2.1, w: 2.78, h: 0.5, align: "center", valign: "middle", fontFace: KF, fontSize: 15, bold: true, color: "FFFFFF" });
    s.addText(c[1], { x: x + 0.15, y: 2.75, w: 2.5, h: 0.4, fontFace: "Consolas", fontSize: 13, bold: true, color: AMBER });
    s.addText(c[2], { x: x + 0.18, y: 3.2, w: 2.45, h: 1.5, fontFace: KF, fontSize: 12.5, color: INK });
    if (i < 3) s.addText("→", { x: x + 2.66, y: 3.0, w: 0.5, h: 0.6, align: "center", fontFace: KF, fontSize: 22, bold: true, color: MUTE });
    x += 3.05;
  });
  s.addText("직교 yaml(rules·recipes·aliases) + canonical metrics 단일구현 + §G 함정 강제(기준자료≠참값·advisory)",
    { x: 0.85, y: 5.5, w: 11.6, h: 0.5, align: "center", fontFace: KF, fontSize: 13, color: MUTE });
  footer(s, 4);
}

// ───────────────────────── S5 데모① 발견+QC ─────────────────────────
{
  const s = p.addSlide();
  header(s, "라이브 데모 ①", "발견(discover) + QC 결함적발");
  s.addImage({ path: "project/presentation/assets/discover_table.png", x: 0.6, y: 2.0, w: 6.05, h: 2.11 });
  s.addImage({ path: "project/presentation/assets/qc_panel.png", x: 6.95, y: 2.06, w: 5.75, h: 2.0 });
  s.addText("① discover — 멀티포맷·도메인 자동 분류", { x: 0.6, y: 4.18, w: 6.05, h: 0.3, fontFace: KF, fontSize: 11, color: MUTE, align: "center" });
  s.addText("② validate — 정상 PASS / 결함 FAIL 근거 적발", { x: 6.95, y: 4.18, w: 5.75, h: 0.3, fontFace: KF, fontSize: 11, color: MUTE, align: "center" });
  s.addText([
    { text: "사용자가 설명 안 해도 ‘무엇이 모델/기준’인지 먼저 파악", options: { bullet: true, breakLine: true } },
    { text: "정상은 통과, 망가뜨린 파일은 근거와 함께 적발 — 실측 완료", options: { bullet: true } },
  ], { x: 0.9, y: 4.7, w: 11.6, h: 0.9, fontFace: KF, fontSize: 13, color: INK, paraSpaceAfter: 4 });
  footer(s, 5);
}

// ───────────────────────── S6 데모② 파랑검증 ─────────────────────────
{
  const s = p.addSlide();
  header(s, "라이브 데모 ②", "파랑 검증 — WW3 모델 vs 부이 관측");
  s.addImage({ path: "project/presentation/assets/wave_validation.png", x: 1.27, y: 1.88, w: 10.8, h: 3.6 });
  s.addText("WW3 vs 부이 · 2024-09-15 · N=393 · 17지점   —   bias −0.12 m · SI 0.43 · R 0.74", { x: 0.9, y: 5.52, w: 11.6, h: 0.32, fontFace: KF, fontSize: 12.5, color: DEEP, align: "center", bold: true });
  s.addText("부이 지점 최근접 매칭 → 정확도·분포·시계열 다축 · 09-15 피크에서 모델 과소(스킬이 좌표 출처를 자동 발견)", { x: 0.9, y: 5.95, w: 11.6, h: 0.5, fontFace: KF, fontSize: 12, color: INK, align: "center" });
  footer(s, 6);
}

// ───────────────────────── S7 재현·전파 ─────────────────────────
{
  const s = p.addSlide();
  header(s, "재현 · 전파", "최고 배점 ②재현·전파성");
  const cols = [
    ["📁 폴더 복사", "스킬은 자기완결 폴더 — 복사만으로 옆 사람 PC에서 동작"],
    ["🛠 yaml만 수정", "새 변수·도메인·기준자료 = 코드 0줄, yaml만 추가"],
    ["📚 부서 자산", "검증 방법 카탈로그(15) + 그림 카탈로그(7도메인) — 따라 할 레시피"],
  ];
  let x = 0.85;
  cols.forEach((c) => {
    card(s, x, 2.1, 3.78, 3.0);
    s.addText(c[0], { x: x + 0.25, y: 2.4, w: 3.3, h: 0.5, fontFace: KF, fontSize: 17, bold: true, color: DEEP });
    s.addText(c[1], { x: x + 0.27, y: 3.0, w: 3.25, h: 1.9, fontFace: KF, fontSize: 13.5, color: INK });
    x += 3.95;
  });
  s.addText("방법론을 ‘한 사람 머릿속’이 아니라 재사용 자산으로 — 이게 전파", { x: 0.85, y: 5.5, w: 11.6, h: 0.5, align: "center", fontFace: KF, fontSize: 15, bold: true, color: TEAL });
  footer(s, 7);
}

// ───────────────────────── S8 효과 (일관성 실측) ─────────────────────────
{
  const s = p.addSlide();
  header(s, "효과 — Before / After", "일관성·재현성 (실측 증거)");
  // 큰 stat 2개
  card(s, 0.85, 2.0, 5.6, 1.7);
  s.addText("재현율", { x: 1.1, y: 2.15, w: 5, h: 0.35, fontFace: KF, fontSize: 13, color: MUTE });
  s.addText([
    { text: "Before ≈ 0%", options: { color: FAIL, bold: true } },
    { text: "  →  ", options: { color: MUTE } },
    { text: "After 100%", options: { color: PASS, bold: true } },
  ], { x: 1.1, y: 2.5, w: 5.2, h: 0.9, fontFace: KF, fontSize: 26, bold: true });
  card(s, 6.85, 2.0, 5.6, 1.7);
  s.addText("같은 결함파일 · 즉석검증 4개", { x: 7.1, y: 2.15, w: 5, h: 0.35, fontFace: KF, fontSize: 13, color: MUTE });
  s.addText([
    { text: "PASS 1 : FAIL 3", options: { bold: true, color: INK } },
    { text: "  (결함 놓침)", options: { color: FAIL } },
  ], { x: 7.1, y: 2.55, w: 5.2, h: 0.8, fontFace: KF, fontSize: 24, bold: true });
  // before/after 표
  s.addTable([
    [{ text: "지표", options: { fill: { color: DEEP }, color: "FFFFFF", bold: true, fontFace: KF } },
     { text: "Before (맨손)", options: { fill: { color: DEEP }, color: "FFFFFF", bold: true, fontFace: KF } },
     { text: "After (스킬)", options: { fill: { color: DEEP }, color: "FFFFFF", bold: true, fontFace: KF } }],
    ["같은 요청 반복", "매번 다름", "매번 동일(바이트까지)"],
    ["검증 항목", "누락 가능", "항상 전 항목"],
    ["결함 적발", "눈으로(놓침)", "자동 + 근거"],
    ["전파·확장", "머릿속", "폴더 복사·yaml"],
  ], {
    x: 0.85, y: 4.0, w: 11.6, colW: [3.0, 4.3, 4.3], rowH: 0.42,
    fontFace: KF, fontSize: 13, color: INK, valign: "middle", align: "left",
    border: { type: "solid", pt: 0.5, color: "D5DEE6" }, fill: { color: "FFFFFF" },
  });
  s.addText("효과를 시간이 아니라 ‘일관성·재현성’으로 측정 — 우리 업무의 진짜 문제였으니까", { x: 0.85, y: 6.65, w: 11.6, h: 0.4, align: "center", fontFace: KF, fontSize: 12, italic: true, color: MUTE });
  footer(s, 8);
}

// ───────────────────────── S9 마무리 ─────────────────────────
{
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addShape(p.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.18, fill: { color: TEAL } });
  s.addShape(p.shapes.OVAL, { x: -1.7, y: 4.0, w: 5.0, h: 5.0, fill: { color: DEEP, transparency: 60 } });
  s.addText("마무리", { x: 0.9, y: 1.3, w: 11, h: 0.4, fontFace: KF, fontSize: 14, color: SKY, bold: true, charSpacing: 2 });
  s.addText([
    { text: "완성된 AI가 아니라,\n", options: { breakLine: true } },
    { text: "반복 수작업을 ", options: {} },
    { text: "일관·재현 가능", options: { color: SKY } },
    { text: "하게 바꾼 도구", options: {} },
  ], { x: 0.9, y: 2.0, w: 11.5, h: 1.8, fontFace: KF, fontSize: 32, bold: true, color: "FFFFFF", lineSpacingMultiple: 1.05 });
  s.addText("“누가 언제 돌려도 같은 검증” — 그게 우리 답입니다.", { x: 0.95, y: 4.0, w: 11, h: 0.5, fontFace: KF, fontSize: 17, color: "C7DCEA" });
  s.addText([
    { text: "정직한 한계  ", options: { bold: true, color: AMBER } },
    { text: "해석 임계는 advisory · 기준자료는 reference(≠참값) · 부이는 대표성오차", options: { color: "9FB4C7" } },
  ], { x: 0.95, y: 5.5, w: 11.4, h: 0.5, fontFace: KF, fontSize: 13 });
}

// ───────────────────────── S10 분담 (부록) ─────────────────────────
{
  const s = p.addSlide();
  header(s, "부록", "발표 분담 — 전원 1인 60초 미니시연");
  s.addTable([
    [{ text: "사람", options: { fill: { color: DEEP }, color: "FFFFFF", bold: true, fontFace: KF } },
     { text: "파트", options: { fill: { color: DEEP }, color: "FFFFFF", bold: true, fontFace: KF } },
     { text: "미니시연", options: { fill: { color: DEEP }, color: "FFFFFF", bold: true, fontFace: KF } }],
    ["A", "문제·통찰", "discover 멀티포맷 분류"],
    ["B", "아키텍처·QC", "QC 정상 PASS / 결함 FAIL 라이브"],
    ["C", "파랑 검증", "WW3↔부이 다축 verify"],
    ["D", "재현·전파·효과", "같은 명령 재실행 → 동일 리포트 + yaml 수정"],
  ], {
    x: 0.85, y: 2.1, w: 11.6, colW: [1.4, 3.6, 6.6], rowH: 0.6,
    fontFace: KF, fontSize: 14, color: INK, valign: "middle",
    border: { type: "solid", pt: 0.5, color: "D5DEE6" }, fill: { color: "FFFFFF" },
  });
  s.addText("본인 프롬프트·결과를 본인 화면에서 라이브로 (공지 규칙) · 데모 실패 대비 사전 녹화 준비", { x: 0.85, y: 5.7, w: 11.6, h: 0.4, align: "center", fontFace: KF, fontSize: 12, italic: true, color: MUTE });
  footer(s, 10);
}

p.writeFile({ fileName: "project/presentation/teamA_pitch_5min.pptx" }).then((f) => console.log("saved:", f));
