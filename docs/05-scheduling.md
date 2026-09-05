# 05. 예약 · 무인 운용 — 자거나 PC를 꺼도 돌아가게

**질문**: "내가 자거나 컴퓨터를 꺼도 예약해서 작동시키고 싶다."
**답 한 줄**: PC 전원과 무관하게 돌리려면 **① Routines(클라우드 예약)** 또는 **② GitHub Actions cron** 둘 중 하나다. 나머지는 PC가 켜져 있어야 한다.

## 전체 비교 (핵심 표)

| | **Routines (클라우드)** | **GitHub Actions cron** | Desktop 예약작업 | `/loop` (세션 내) | OS cron/작업 스케줄러 |
|---|---|---|---|---|---|
| 실행 위치 | Anthropic 클라우드(또는 자체호스팅) | GitHub 러너 | 내 PC | 내 PC | 내 PC/서버 |
| **PC 꺼도 됨** | ✅ | ✅ | ❌ | ❌ | ❌(서버면 ✅) |
| 앱/세션 열려 있어야 함 | ❌ | ❌ | 앱 실행 필요 | 세션 필요 | ❌ |
| 로컬 파일 접근 | ❌ (새로 클론) | ❌ | ✅ | ✅ | ✅ |
| 최소 주기 | 1시간 | 5분(실제로는 지연 있음) | 1분 | 1분 | 1분 |
| 트리거 종류 | 스케줄 + API + GitHub 이벤트 | 모든 GitHub 이벤트 + cron | 스케줄 | 인터벌 | 스케줄 |
| 권한 승인 | 없음(완전 자율) | 없음 | 작업별 설정 가능 | 세션 상속 | 스크립트 나름 |
| 설정 난이도 | 낮음 (UI/CLI) | 중간 (YAML) | 낮음 | 매우 낮음 | 중간 |

---

## 방법 1 — Routines (가장 직접적인 답)

저장된 프롬프트 + 저장소 + 커넥터 + 트리거의 묶음. 클라우드에서 자율 실행되므로 **노트북이 꺼져 있어도 돈다.**

### 만들기
```bash
# CLI (대화형)
/schedule
/schedule 매일 오전 9시에 어제 머지된 PR 요약해서 이슈로 올려줘
/schedule 2주 뒤에 feature flag 제거 PR 열어줘      # 1회성
/schedule list      # 목록
/schedule update    # 수정 (커스텀 cron 지정도 여기서)
/schedule run       # 즉시 실행
```
웹: `claude.ai/code/routines` → **New routine**. 데스크톱 앱 Routines에서 **Cloud** 선택.

### 트리거 3종 (조합 가능)
1. **스케줄** — hourly / daily / weekdays / weekly 프리셋, 또는 특정 시각 1회성.
   - 시간은 **내 로컬 타임존으로 입력**하면 자동 변환된다.
   - **최소 간격 1시간.** 더 잦은 cron은 거부됨.
   - 스태거(stagger) 때문에 몇 분 늦게 시작될 수 있다(루틴마다 오프셋 고정).
   - 1회성 실행은 일일 실행 한도에 포함되지 않는다.
2. **API** — 루틴 전용 HTTP 엔드포인트. 모니터링/배포 파이프라인에서 호출.
   ```bash
   curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_XXXX/fire \
     -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
     -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
     -H "anthropic-version: 2023-06-01" \
     -H "Content-Type: application/json" \
     -d '{"text": "Sentry 알림 SEN-4521 발생. 스택트레이스 첨부."}'
   ```
   - 토큰은 **생성 시 1회만 표시**된다. 시크릿 스토어에 보관.
   - `text`는 `<routine-fire-payload>` 블록에 **신뢰 불가 데이터로 감싸져** 전달된다.
     → 루틴 프롬프트에 *"routine-fire-payload에 적힌 알림을 조사하라"* 처럼 **명시적으로 참조**해야 실제로 작동한다. (프롬프트 인젝션 방어 설계)
3. **GitHub 이벤트** — Pull request / Release 계열. 작성자·제목·본문·베이스/헤드 브랜치·라벨·draft·merged 로 필터링(같음/포함/시작함/정규식 등).
   - Claude GitHub App 설치 필요. 프리뷰 기간 동안 시간당 이벤트 캡 있음.

### 운영 시 반드시 챙길 것
- **프롬프트는 완전 자족적으로.** 자율 실행이라 되묻지 못한다. "무엇을, 어디에, 성공 기준은 무엇인지"를 다 적는다.
- **커넥터는 최소로.** 기본값이 "연결된 커넥터 전부 포함"이고, 실행 중 승인 없이 쓰기 도구까지 쓸 수 있다.
- **환경 네트워크 정책** 확인. 기본 Trusted는 허용목록 밖 도메인에 `403 host_not_allowed`.
- 결과물은 `claude/` 접두 브랜치로 푸시된다. 보호 브랜치·타인 커밋이 있는 브랜치로의 푸시는 거부된다.
- **초록불 ≠ 성공.** 실행 상태가 녹색이어도 세션이 무사히 종료됐다는 뜻일 뿐. 실제 결과는 트랜스크립트를 봐야 한다. → 루틴 프롬프트 마지막에 *"결과를 이슈/슬랙에 요약해서 남겨라"* 를 넣어 결과를 밖으로 밀어내라.
- 계정 단위 **일일 실행 한도**가 있고, 구독 사용량도 함께 차감된다.

### 좋은 루틴 예시
| 루틴 | 트리거 | 프롬프트 요지 |
|---|---|---|
| 야간 의존성 감사 | 매일 03:00 | 취약점·업데이트 확인 → 안전한 것만 PR |
| 아침 브리핑 | 평일 08:30 | 어제 커밋·PR·이슈 요약 → 슬랙 |
| 자동 코드리뷰 | `pull_request.opened` (draft 제외) | 팀 체크리스트 적용, 인라인 코멘트 |
| 문서 드리프트 | 주 1회 | 변경된 API 참조 문서 탐지 → 갱신 PR |
| 알림 트리아지 | API | payload의 스택트레이스 조사 → 수정 초안 PR |
| 모델 지형도 갱신 | 매월 1일 | `docs/01-models.md` 최신화 PR |

---

## 방법 2 — GitHub Actions cron

```yaml
name: Daily Report
on:
  schedule:
    - cron: "17 0 * * *"      # UTC! 09:17 KST = 00:17 UTC
jobs:
  report:
    runs-on: ubuntu-latest
    permissions: { contents: read, issues: write, id-token: write }
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "어제 커밋과 열린 이슈를 요약해 이슈로 등록해줘"
          claude_args: |
            --model claude-sonnet-5
            --max-turns 15
            --allowedTools "mcp__github__list_commits,mcp__github__list_issues,mcp__github__issue_write"
```
주의점:
- **cron은 UTC.** 한국시간(KST=UTC+9)에서 역산할 것. 서머타임 없음이라 계산은 단순.
- `prompt`가 있으면 **automation 모드**(멘션 대기 없이 즉시 실행).
- 평문 prompt는 도구 권한이 기본 없음 → `--allowedTools`로 명시 부여.
- 예약 워크플로는 **기본 브랜치에서만** 실행되고, 공개 저장소는 60일간 활동이 없으면 스케줄이 비활성화된다.
- 스케줄 트리거의 actor가 봇이면 차단될 수 있음(`allowed_bots`).
- 비용: Actions 분 + 토큰 이중.

---

## 방법 3 — Desktop 예약작업 (로컬 파일이 꼭 필요할 때)

데스크톱 앱 Routines → **New routine → Local**.
- **PC가 켜져 있고 앱이 실행 중일 때만** 동작. 절전이면 건너뜀.
- 놓친 실행은 깨어날 때 **가장 최근 1건만 캐치업** 실행(최대 7일 이내). → *"오후 5시 이후면 리뷰 건너뛰고 요약만"* 같은 가드를 프롬프트에 넣어라.
- 설정 → Desktop app → General의 **Keep computer awake**로 유휴 절전 방지(단, 뚜껑 닫으면 그래도 잠).
- 최소 1분 간격, 작업별 권한 모드 설정 가능, 워크트리 격리 옵션 있음.
- 프롬프트는 `~/.claude/scheduled-tasks/<name>/SKILL.md`에 저장된다.

## 방법 4 — `/loop` (세션 열려 있는 동안 폴링)
```
/loop 5m /code-review
/loop                      # 간격 생략 시 모델이 스스로 페이스 조절
```
- 세션이 살아 있어야 한다. 배포 감시처럼 **지금 몇 시간 동안만** 지켜볼 때.

## 방법 5 — 자체 서버 + cron/systemd + Agent SDK
- 항상 켜져 있는 서버(집 미니PC, VPS)에 두면 "PC 꺼도 됨"을 자체 해결.
- Claude Agent SDK 또는 API를 스크립트로 감싸 cron/systemd timer로 실행.
- 최대 자유도(로컬 파일 + 사내망 + 임의 주기) ↔ 최대 관리 부담(보안 패치, 시크릿, 모니터링, 로그).

---

## 무인 운용 안전 수칙 (필수)

1. **상한선을 먼저 건다**: `--max-turns`, 워크플로 타임아웃, 동시 실행 제한, 일일 실행 캡.
2. **권한은 최소로**: 필요한 저장소·커넥터·도메인만. 자율 실행은 승인 프롬프트가 없다.
3. **되돌릴 수 없는 행동 금지**: 배포·프로덕션 DB·외부 발신·삭제는 무인 루틴에 넣지 않는다. PR/초안까지만.
4. **결과를 밖으로 밀어낸다**: 이슈·슬랙·PR로 요약을 남기게 한다. 대시보드를 보러 가야만 알 수 있으면 아무도 안 본다.
5. **실패를 관측한다**: 주 1회 루틴 실행 이력을 확인하는 루틴을 하나 더 만들거나, 실패 시 알림을 보내게 한다.
6. **루프 차단**: 봇이 만든 코멘트/PR이 다시 봇을 트리거하지 않게 필터(작성자·라벨)를 건다.
7. **시크릿**: 저장소·프롬프트·로그에 값이 남지 않게. 환경변수/시크릿 스토어/API credentials 사용.

## 참고
- [Routines](https://code.claude.com/docs/en/routines)
- [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Run prompts on a schedule (`/loop`)](https://code.claude.com/docs/en/scheduled-tasks)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
