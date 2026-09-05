#!/usr/bin/env python3
"""
인역 캐논 references에 '요약 + 행번호 목차' 헤더를 얹는다.

목적: 에이전트가 60KB 설정집을 통독하지 않고,
      헤더만 읽은 뒤 `sed -n 'A,Bp' file.md` 로 필요한 구간만 읽게 한다.

원문은 수정하지 않는다. 파일 맨 위에 CANON-INDEX 블록만 추가/교체한다.
재실행해도 블록이 쌓이지 않는다(idempotent).

사용:
  python3 scripts/canon_index.py <references_dir> [--check]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARIES = {}


def load_summaries(path=None):
    global SUMMARIES
    SUMMARIES = json.load(
        open(path or os.path.join(HERE, "canon-summaries.json"), encoding="utf-8")
    )

BEGIN = "<!-- CANON-INDEX v1 -->"
END = "<!-- /CANON-INDEX -->"

# 유사 헤딩: **제목** 한 줄 통째 (DOCX 변환 산물) 또는 진짜 마크다운 헤딩
RE_BOLD = re.compile(r"^\*\*\s*(.{1,70}?)\s*\*\*\s*$")
RE_ATX = re.compile(r"^(#{1,3})\s+(.+?)\s*$")

# 목차에 넣지 않을 표지/장식 줄
NOISE = {"人域", "인역", "人 域", "설정집", "목차", "개요"}

# 대분류로 볼 제목 패턴
RE_MAJOR = re.compile(
    r"^(?:\d+\.\s|\d+-\d+\.\s|파트\s*\d|Axis\s|Lv\.\d|제\d+법칙|▶\s|▣\s)"
)


def is_noise(title: str) -> bool:
    t = title.strip()
    return (
        t in NOISE
        or len(t) <= 3
        or t.isdigit()
        or re.fullmatch(r"[\d\s\-.]+", t) is not None
    )


def clean_title(title: str) -> str:
    """DOCX 변환 잔재를 걷어낸다: 굵게 표시, 이스케이프, 중복 공백."""
    t = title.replace("**", "").replace("\\", "")
    return re.sub(r"\s{2,}", " ", t).strip(" :·-")


def sanitize(title: str) -> str:
    """HTML 주석 안에서 안전하도록 하이픈 연쇄를 em dash 로 접는다."""
    t = re.sub(r"-{2,}", "—", clean_title(title))
    return t.replace(">", "＞").strip()


def collect_headings(lines):
    """[(lineno_1based, level, title)] — level 0=대분류, 1=소분류"""
    out = []
    for i, line in enumerate(lines, start=1):
        m = RE_ATX.match(line)
        if m:
            title = clean_title(m.group(2))
            if is_noise(title):
                continue
            out.append((i, 0 if len(m.group(1)) <= 2 else 1, title))
            continue
        m = RE_BOLD.match(line)
        if m:
            title = clean_title(m.group(1))
            if is_noise(title):
                continue
            out.append((i, 0 if RE_MAJOR.match(title) else 1, title))
    return out


def build_block(name, body_lines, headings, offset):
    """offset = 헤더가 앞에 붙은 뒤 원문 줄이 밀리는 양"""
    total = len(body_lines) + offset
    rows = []
    for idx, (ln, level, title) in enumerate(headings):
        start = ln + offset
        end = (headings[idx + 1][0] + offset - 1) if idx + 1 < len(headings) else total
        indent = "  " if level else ""
        rows.append(f"  {indent}L{start}-{end}  {sanitize(title)}")

    summary = SUMMARIES.get(name, "(요약 미작성 — scripts/canon-summaries.json 에 추가할 것)")
    lines = [
        BEGIN,
        "<!-- 이 블록만 읽고, 필요한 구간을 `sed -n 'A,Bp'` 로 부분 읽기 할 것.",
        "     전체 통독은 마지막 수단. 행 번호는 이 헤더를 포함한 값이다. -->",
        f"<!-- SUMMARY: {sanitize(summary)} -->",
        f"<!-- STATS: {total} lines -->",
        "<!-- TOC",
        *rows,
        "-->",
        END,
        "",
    ]
    return lines


def strip_existing(lines):
    if not lines or not lines[0].startswith(BEGIN):
        return lines
    for i, line in enumerate(lines):
        if line.strip() == END:
            j = i + 1
            if j < len(lines) and lines[j].strip() == "":
                j += 1
            return lines[j:]
    return lines


def process(path, check=False):
    name = os.path.basename(path)
    raw = open(path, encoding="utf-8").read().split("\n")
    body = strip_existing(raw)
    headings = collect_headings(body)
    if not headings:
        return name, 0, "헤딩 없음 — 건너뜀"

    # 헤더 줄 수는 목차 항목 수로 결정되므로 2-pass 로 오프셋을 확정한다.
    offset = len(build_block(name, body, headings, 0))
    block = build_block(name, body, headings, offset)
    assert len(block) == offset, "헤더 줄 수가 흔들림"

    new = "\n".join(block + body)
    if check:
        cur = "\n".join(raw)
        return name, len(headings), ("최신" if cur == new else "갱신 필요")
    open(path, "w", encoding="utf-8").write(new)
    return name, len(headings), "OK"


def main():
    argv = sys.argv[1:]
    check = "--check" in argv
    no_index = "--no-index" in argv

    summaries_path = None
    if "--summaries" in argv:
        summaries_path = argv[argv.index("--summaries") + 1]
    load_summaries(summaries_path)

    dirs = [
        a
        for i, a in enumerate(argv)
        if not a.startswith("--") and (i == 0 or argv[i - 1] != "--summaries")
    ]
    if not dirs:
        sys.exit("사용법: canon_index.py <dir> [<dir>...] [--summaries PATH] [--no-index] [--check]")

    for ref_dir in dirs:
        targets = sorted(
            f for f in os.listdir(ref_dir)
            if f.endswith(".md") and f != "INDEX.md"
        )
        if not targets:
            continue
        print(f"[{ref_dir}]")
        results = [process(os.path.join(ref_dir, f), check) for f in targets]
        width = max(len(r[0]) for r in results)
        for name, n, status in results:
            print(f"  {name:<{width}}  섹션 {n:>3}개  {status}")

        if not check and not no_index:
            write_index(ref_dir, targets)
            print(f"  INDEX.md 생성 ({len(targets)}개 파일)")
        print()


def write_index(ref_dir, targets):
    lines = [
        "<!-- 자동 생성: scripts/canon_index.py — 직접 수정하지 말 것 -->",
        "# 인역 캐논 인덱스",
        "",
        "**작업 시작 시 이 파일을 먼저 읽는다.** 어떤 설정집의 어느 구간이 필요한지 정한 뒤,",
        "해당 파일의 `CANON-INDEX` 헤더(맨 위)를 보고 `sed -n 'A,Bp'` 로 그 구간만 읽는다.",
        "설정집 전체를 통독하는 것은 마지막 수단이다.",
        "",
        "| 파일 | 크기 | 내용 |",
        "|---|---|---|",
    ]
    # 정본을 맨 위로 올린다 — 목록에서 묻히면 안 된다.
    ordered = sorted(targets, key=lambda f: (f != "innyeok.md", f))
    for f in ordered:
        size = os.path.getsize(os.path.join(ref_dir, f))
        summary = SUMMARIES.get(f, "(요약 미작성)")
        lines.append(f"| `{f}` | {size // 1024}KB | {summary} |")
    lines += [
        "",
        "## 읽기 순서 원칙",
        "",
        "1. `innyeok.md` 가 정본이다. 다른 설정집과 충돌하면 정본이 이긴다.",
        "   파일명은 개정(v4·v5…)과 무관하게 고정이다. 개정 번호는 문서 안에 적힌다.",
        "2. 필요한 파일만, 필요한 구간만 읽는다.",
        "3. 구버전(v2·v3)은 `archive/` 에 있다. **절대 참조하지 않는다.**",
        "",
    ]
    open(os.path.join(ref_dir, "INDEX.md"), "w", encoding="utf-8").write("\n".join(lines))


if __name__ == "__main__":
    main()
