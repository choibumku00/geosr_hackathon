// 시연 walkthrough PPT — 평이한 말(구현용어 배제), 단계 흐름 구성
const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
p.author = "A팀";
p.title = "시연 — 한 줄 명령으로 수치모델 검증";

const W = 13.33;
const KF = "Malgun Gothic", MONO = "Consolas";
const DARK = "0B3B3F", TEAL = "0E7C86", SEA = "2BB7AE", SKY = "9FD8D5";
const LIGHT = "F2F7F7", INK = "17313A", MUTE = "5B7185";
const GOOD = "1E8449", UNDER = "C0392B", AMBER = "C9760F";
const sh = () => ({ type: "outer", color: "08272A", blur: 8, offset: 3, angle: 135, opacity: 0.15 });

function header(s, step, title) {
  s.background = { color: LIGHT };
  // 단계 배지
  s.addShape(p.shapes.OVAL, { x: 0.55, y: 0.5, w: 0.62, h: 0.62, fill: { color: TEAL } });
  s.addText(step, { x: 0.55, y: 0.5, w: 0.62, h: 0.62, align: "center", valign: "middle", fontFace: KF, fontSize: 17, bold: true, color: "FFFFFF" });
  s.addText(title, { x: 1.35, y: 0.5, w: 11.4, h: 0.7, fontFace: KF, fontSize: 26, bold: true, color: INK, valign: "middle" });
}
function foot(s, n) {
  s.addText("A팀 · 시연", { x: 0.55, y: 7.06, w: 6, h: 0.3, fontFace: KF, fontSize: 9, color: MUTE });
  s.addText(String(n), { x: 12.4, y: 7.06, w: 0.5, h: 0.3, fontFace: KF, fontSize: 9, color: MUTE, align: "right" });
}
function card(s, x, y, w, h, fill) {
  s.addShape(p.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill || "FFFFFF" }, rectRadius: 0.08, shadow: sh() });
}

// ── S1 타이틀 ──
{
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addShape(p.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.16, fill: { color: SEA } });
  s.addShape(p.shapes.OVAL, { x: 10.0, y: -1.8, w: 5.6, h: 5.6, fill: { color: TEAL, transparency: 55 } });
  s.addText("시연 (Live Demonstration)", { x: 0.9, y: 1.45, w: 11, h: 0.4, fontFace: KF, fontSize: 15, color: SKY, bold: true, charSpacing: 1 });
  s.addText([
    { text: "한 줄 명령으로\n", options: { breakLine: true } },
    { text: "수치모델을 ", options: {} },
    { text: "스스로 검증", options: { color: SEA } },
    { text: "하다", options: {} },
  ], { x: 0.9, y: 2.05, w: 11.4, h: 2.0, fontFace: KF, fontSize: 40, bold: true, color: "FFFFFF", lineSpacingMultiple: 1.05 });
  s.addText("AI 에이전트가 자료를 파악하고, 부족한 정보를 스스로 채워 검증한다", { x: 0.95, y: 4.45, w: 11.2, h: 0.5, fontFace: KF, fontSize: 16, color: "CDE7E5" });
  s.addText("A팀", { x: 0.95, y: 5.7, w: 11, h: 0.4, fontFace: KF, fontSize: 13, color: MUTE });
}

// ── S2 명령 한 줄 ──
{
  const s = p.addSlide();
  header(s, "▶", "어떻게 시작하나 — 자연어 한 줄");
  // 터미널 박스
  s.addShape(p.shapes.ROUNDED_RECTANGLE, { x: 1.1, y: 2.2, w: 11.1, h: 1.7, fill: { color: "0B3B3F" }, rectRadius: 0.06, shadow: sh() });
  s.addText([
    { text: "/validate-model-output", options: { color: SEA, bold: true } },
    { text: "  이 폴더의 파랑모델을 부이 관측으로 검증해줘", options: { color: "EAF6F5" } },
  ], { x: 1.45, y: 2.55, w: 10.5, h: 0.7, fontFace: MONO, fontSize: 17 });
  s.addText("커서 깜빡임 한 줄 — 폴더 경로만 주면 끝. 어떤 분석을 어떻게 할지 일일이 지정하지 않는다.",
    { x: 1.45, y: 3.25, w: 10.5, h: 0.5, fontFace: KF, fontSize: 13, color: SKY });
  s.addText("→ 사용자가 하는 일은 여기까지. 나머지는 에이전트가 스스로 진행한다.",
    { x: 1.1, y: 4.5, w: 11.1, h: 0.5, align: "center", fontFace: KF, fontSize: 16, bold: true, color: TEAL });
  foot(s, 2);
}

// ── S3 1단계 자료 파악 ──
{
  const s = p.addSlide();
  header(s, "1", "폴더를 훑어 ‘무엇이 있는지’ 자동 정리");
  s.addImage({ path: "project/presentation/assets/inventory_plain.png", x: 1.7, y: 1.95, w: 9.9, h: 2.88 });
  s.addText([
    { text: "어떤 게 검증할 모델이고 어떤 게 비교 기준(관측)인지 스스로 구분", options: { bullet: true, breakLine: true } },
    { text: "자료 형식이 서로 달라도(격자/지점, 한글/영문) 알아서 읽어 들임", options: { bullet: true } },
  ], { x: 1.0, y: 5.2, w: 11.4, h: 1.0, fontFace: KF, fontSize: 14, color: INK, paraSpaceAfter: 5 });
  foot(s, 3);
}

// ── S4 2단계 빠진 정보 스스로 보완 (핵심) ──
{
  const s = p.addSlide();
  header(s, "2", "빠진 정보를 스스로 찾아 채운다  (핵심)");
  const steps = [
    ["관측자료", "‘위치’ 정보가 없음", "FCEDEC", UNDER],
    ["같은 폴더를 살펴봄", "위치 목록을 발견", "EAF3EE", TEAL],
    ["자동 연결", "관측 ↔ 가까운 모델 지점", "E7F4EE", GOOD],
  ];
  let x = 0.85;
  steps.forEach((c, i) => {
    card(s, x, 2.2, 3.55, 2.0, c[2]);
    s.addText(c[0], { x: x + 0.2, y: 2.5, w: 3.15, h: 0.5, fontFace: KF, fontSize: 16, bold: true, color: INK });
    s.addText(c[1], { x: x + 0.2, y: 3.1, w: 3.15, h: 0.8, fontFace: KF, fontSize: 14, color: c[3] });
    if (i < 2) s.addText("→", { x: x + 3.5, y: 2.9, w: 0.55, h: 0.6, align: "center", fontFace: KF, fontSize: 26, bold: true, color: MUTE });
    x += 4.05;
  });
  s.addText("사람이 ‘위치는 저기 있어’라고 알려주지 않아도, 부족한 정보를 폴더에서 찾아 메운다.",
    { x: 0.85, y: 4.7, w: 11.6, h: 0.5, align: "center", fontFace: KF, fontSize: 16, bold: true, color: TEAL });
  s.addText("바로 이 점이 ‘그냥 챗봇에 시키기’와 다른 부분 — 자료 사정을 스스로 파악해 적응한다.",
    { x: 0.85, y: 5.4, w: 11.6, h: 0.5, align: "center", fontFace: KF, fontSize: 13, color: MUTE });
  foot(s, 4);
}

// ── S5 3단계 비교·검증 ──
{
  const s = p.addSlide();
  header(s, "3", "모델과 관측을 맞춰 차이를 계산");
  const items = [
    ["같은 지점", "관측 지점마다 가장 가까운 모델 값을 가져온다"],
    ["같은 시각", "관측 시각에 맞는 모델 시각을 짝짓는다"],
    ["차이 계산", "유의파고 차이를 모아 통계·그림으로 정리"],
  ];
  let y = 1.95;
  items.forEach((it, i) => {
    card(s, 1.4, y, 10.5, 1.25);
    s.addShape(p.shapes.OVAL, { x: 1.75, y: y + 0.32, w: 0.6, h: 0.6, fill: { color: TEAL } });
    s.addText(String(i + 1), { x: 1.75, y: y + 0.32, w: 0.6, h: 0.6, align: "center", valign: "middle", fontFace: KF, fontSize: 17, bold: true, color: "FFFFFF" });
    s.addText(it[0], { x: 2.6, y: y + 0.2, w: 9.0, h: 0.45, fontFace: KF, fontSize: 17, bold: true, color: INK });
    s.addText(it[1], { x: 2.6, y: y + 0.66, w: 9.0, h: 0.45, fontFace: KF, fontSize: 13.5, color: MUTE });
    y += 1.45;
  });
  foot(s, 5);
}

// ── S6 결과 숫자 ──
{
  const s = p.addSlide();
  header(s, "✓", "검증 결과 — 파랑모델 vs 부이 (5일)");
  const stats = [
    ["비교한 자료 수", "1,956", "건", INK],
    ["평균 차이", "−0.39", "m (모델이 낮음)", UNDER],
    ["오차 크기(RMSE)", "0.59", "m", INK],
    ["상관", "0.77", "", GOOD],
  ];
  let x = 0.85;
  stats.forEach((c) => {
    card(s, x, 2.1, 2.85, 1.9);
    s.addText(c[0], { x: x + 0.2, y: 2.28, w: 2.5, h: 0.4, fontFace: KF, fontSize: 12.5, color: MUTE });
    s.addText(c[1], { x: x + 0.2, y: 2.72, w: 2.5, h: 0.8, fontFace: KF, fontSize: 32, bold: true, color: c[3] });
    s.addText(c[2], { x: x + 0.2, y: 3.55, w: 2.55, h: 0.35, fontFace: KF, fontSize: 11, color: MUTE });
    x += 3.05;
  });
  card(s, 0.85, 4.4, 11.6, 1.4, "EAF3EE");
  s.addText("핵심 발견", { x: 1.15, y: 4.6, w: 3, h: 0.4, fontFace: KF, fontSize: 14, bold: true, color: TEAL });
  s.addText("파고가 높은 지점·시기일수록 모델이 관측보다 낮게 모의 — 큰 파도를 과소평가하는 경향.",
    { x: 1.15, y: 5.0, w: 11.0, h: 0.7, fontFace: KF, fontSize: 15, color: INK });
  foot(s, 6);
}

// ── S7 결과 그림 ──
{
  const s = p.addSlide();
  header(s, "✓", "검증 결과 — 그림으로 보기");
  s.addImage({ path: "project/presentation/assets/wave_result.png", x: 1.27, y: 1.95, w: 10.8, h: 3.6 });
  s.addText("왼쪽: 모델·관측 비교(점이 선 아래로 치우치면 모델이 낮음)  ·  가운데: 한 지점 시간변화(큰 파도에서 차이 큼)  ·  오른쪽: 분포 비교",
    { x: 0.85, y: 5.7, w: 11.6, h: 0.6, align: "center", fontFace: KF, fontSize: 12.5, color: MUTE });
  foot(s, 7);
}

// ── S8 정직한 한계 ──
{
  const s = p.addSlide();
  header(s, "!", "정직하게 — 이렇게 읽어야 한다");
  const lim = [
    ["기준은 ‘정답’이 아니다", "관측도 오차가 있다 — ‘모델이 틀렸다’가 아니라 ‘모델과 관측의 차이’로 읽는다"],
    ["좋다/나쁘다 단정 금지", "잘 맞는지 기준선은 해역·상황에 따라 달라진다 — 참고용으로만"],
    ["일부 지점·한 사례", "위치를 아는 지점만, 특정 기간만 본 결과다"],
  ];
  let y = 1.95;
  lim.forEach((it) => {
    card(s, 0.85, y, 11.6, 1.25, "FFFDF7");
    s.addShape(p.shapes.RECTANGLE, { x: 0.85, y: y, w: 0.14, h: 1.25, fill: { color: AMBER } });
    s.addText(it[0], { x: 1.2, y: y + 0.2, w: 11.0, h: 0.45, fontFace: KF, fontSize: 16, bold: true, color: INK });
    s.addText(it[1], { x: 1.2, y: y + 0.68, w: 11.0, h: 0.45, fontFace: KF, fontSize: 13, color: MUTE });
    y += 1.45;
  });
  foot(s, 8);
}

// ── S9 의미·마무리 ──
{
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addShape(p.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.16, fill: { color: SEA } });
  s.addShape(p.shapes.OVAL, { x: -1.8, y: 3.8, w: 5.2, h: 5.2, fill: { color: TEAL, transparency: 55 } });
  s.addText("이 시연이 보여준 것", { x: 0.9, y: 1.3, w: 11, h: 0.4, fontFace: KF, fontSize: 14, color: SKY, bold: true, charSpacing: 1 });
  s.addText([
    { text: "같은 명령이면\n", options: { breakLine: true } },
    { text: "누가·언제 해도 ", options: {} },
    { text: "같은 검증", options: { color: SEA } },
  ], { x: 0.9, y: 1.95, w: 11.4, h: 1.7, fontFace: KF, fontSize: 34, bold: true, color: "FFFFFF", lineSpacingMultiple: 1.05 });
  s.addText([
    { text: "✓  자료 사정을 스스로 파악·보완해 검증한다", options: { breakLine: true, color: "EAF6F5" } },
    { text: "✓  파랑이 아닌 다른 자료·분야에도 같은 방식으로 확장된다", options: { color: "EAF6F5" } },
  ], { x: 0.95, y: 4.1, w: 11.2, h: 1.2, fontFace: KF, fontSize: 16, paraSpaceAfter: 8 });
  s.addText("반복 검증 업무를, 누구나 똑같이 재현할 수 있게.", { x: 0.95, y: 5.7, w: 11, h: 0.4, fontFace: KF, fontSize: 13, italic: true, color: SKY });
}

p.writeFile({ fileName: "project/presentation/teamA_demo_walkthrough.pptx" }).then((f) => console.log("saved:", f));
