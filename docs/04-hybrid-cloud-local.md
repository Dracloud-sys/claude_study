# 04. 클라우드 ↔ 로컬 병행 운용

**질문**: "클라우드와 로컬을 아울러 작업하고 싶다."
**답**: 네 가지 방식이 있고, 실제로는 **방식 A(왕복 핸드오프)를 기본으로 두고 D(로컬 모델)를 예외 처리에 쓰는 조합**이 가장 실용적이다.

---

## 방식 A — Claude Code 세션 왕복 (권장 기본값)

로컬 CLI와 클라우드 세션 사이를 오가는 방식. 상태는 **git**으로 넘어간다.

### A-1. 로컬 → 클라우드
```bash
# 1) 로컬에서 계획만 세운다 (파일 수정 안 함)
claude --permission-mode plan
#    계획을 docs/plans/migration.md 로 저장 → commit → push

# 2) 실행은 클라우드에 위임
claude --cloud "docs/plans/migration.md 의 계획을 실행해줘"

# 3) 여러 작업 병렬로 던지기
claude --cloud "auth.spec.ts 의 flaky 테스트 수정"
claude --cloud "API 문서 갱신"
```
- 클라우드 VM은 **내 로컬 체크아웃이 아니라 GitHub 리모트의 현재 브랜치를 클론**한다 → **푸시 먼저**.
- GitHub에 없는 로컬 저장소도 번들로 업로드 가능(100MB 제한, untracked 파일 제외, 자격증명류 파일은 자동 제외).

### A-2. 진행 확인 / 추가 지시
```bash
claude                      # 세션 안에서
/tasks                      # 백그라운드 세션 목록·진행 상황
claude -p "테스트도 추가해줘" --cloud session_01ABC...   # 어느 머신에서든 후속 메시지 전송
```
- 브라우저(claude.ai/code)와 모바일 앱에서도 같은 세션을 보고 조종할 수 있다. **노트북을 닫아도 계속 돈다.**

### A-3. 클라우드 → 로컬 (teleport)
```bash
claude --teleport            # 세션 선택 UI
claude --teleport session_01ABC...
# 세션 안에서는 /teleport 또는 /tp, /tasks 에서 t 키
```
- 클라우드 세션의 **브랜치를 체크아웃하고 대화 히스토리까지 로컬로 가져온다.**
- 조건: 작업트리 깨끗할 것, 같은 저장소 체크아웃일 것, 브랜치가 푸시되어 있을 것, 같은 계정일 것.
- 주의: 텔레포트 후 로컬 작업은 **로컬에만** 남는다(클라우드 세션에 역반영 안 됨). 계속 폰으로 보려면 로컬에서 `/remote-control`.

### A-4. 클라우드 환경 구성
클라우드 세션이 도는 "환경"에서 다음을 설정한다:
- **네트워크 접근 수준**: Trusted(기본 허용목록: 패키지 레지스트리 등) / Custom(도메인 지정) / Full / 차단
- **환경변수**와 **API 자격증명**(Pro/Max에서는 샌드박스 밖에 보관되어 세션이 값을 못 봄)
- **셋업 스크립트**: 의존성 설치. 결과가 캐시되어 매번 재실행되지 않음
- 조직은 **자체 호스팅 환경(self-hosted)** 으로 자기 인프라에서 돌릴 수도 있다

### 장단점
| 장점 | 단점 |
|---|---|
| 로컬 자원 안 씀, 노트북 닫아도 진행 | GitHub 의존(GitLab/Bitbucket은 푸시 불가, 번들만) |
| 병렬 작업 자유롭게 확장 | 로컬 파일·로컬 DB·사내망 직접 접근 불가 |
| 모바일에서 감시·조종 가능 | 사용량 한도를 공유하므로 병렬 = 한도 소모 |
| 계정 격리된 VM, 자격증명 샌드박스 밖 보관 | 컨텍스트 이관은 git 경유라 커밋 규율 필요 |
| 계획(로컬)/실행(클라우드) 분리로 비용·품질 균형 | IP 허용목록 쓰는 조직은 별도 예외 필요 |

---

## 방식 B — GitHub를 허브로 (에이전트가 아니라 저장소를 중심에)

로컬 개발 + `@claude` 멘션/Actions + 클라우드 세션이 **전부 같은 PR 위에서** 만난다.

```yaml
# .github/workflows/claude.yml  — 이슈/PR 코멘트에 @claude 로 호출
on:
  issue_comment: { types: [created] }
  pull_request_review_comment: { types: [created] }
jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write, issues: write, id-token: write, actions: read }
    steps:
      - uses: actions/checkout@v6
      - uses: anthropics/claude-code-action@v1
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```
- 설정: 로컬에서 `/install-github-app` 실행하면 앱 설치 + 시크릿 + 워크플로 PR까지 자동.
- 인증: `ANTHROPIC_API_KEY`(콘솔 키) 또는 `CLAUDE_CODE_OAUTH_TOKEN`(`claude setup-token`, 구독 사용). 조직은 OIDC 연합(workload identity federation)으로 장기 시크릿 없이도 가능.
- **PR 자동 수정(Auto-fix)**: PR의 CI 실패·리뷰 코멘트에 클라우드 세션이 자동 반응. 로컬에서 `/autofix-pr`, 또는 웹 CI 바에서 토글.

| 장점 | 단점 |
|---|---|
| 어디서 일하든 결과가 PR 한 곳에 모임 | GitHub 전제 |
| 팀 전체가 같은 인터페이스(코멘트) 사용 | Actions 분(minutes) + 토큰 이중 과금 |
| 감사 추적이 자동으로 남음 | 워크플로 권한 설계 필요(과다 권한 주의) |
| 이슈 → PR 자동화가 자연스러움 | 코멘트 기반 자동화(Atlantis 등)와 루프 위험 |

---

## 방식 C — 로컬 CLI + 원격 감시 (Remote Control)

로컬에서 세션을 돌리되 **웹/모바일에서 들여다보고 지시**한다.
```bash
claude --remote-control      # 또는 세션 안에서 /remote-control
```
- 실행은 내 머신(로컬 파일·사내망·로컬 DB 접근 가능), 조종은 어디서나.
- `--cloud`와 혼동 금지: `--cloud`는 클라우드에서 실행, `--remote-control`은 로컬 실행 + 원격 조종.

| 장점 | 단점 |
|---|---|
| 로컬 자원·사내망·비공개 데이터 그대로 사용 | 내 컴퓨터가 켜져 있어야 함 |
| 외출 중에도 진행 확인·개입 | 로컬 자원 점유(빌드 중 노트북 느려짐) |
| 클라우드 환경 구성 불필요 | 정전/절전 시 중단 |

---

## 방식 D — 로컬 모델 (오프라인·민감 데이터)

Ollama / LM Studio / vLLM으로 오픈웨이트 모델을 로컬에 띄우고, 코딩 에이전트나 자체 스크립트를 붙인다.

- 용도: **외부로 나가면 안 되는 데이터**, 오프라인 환경, 대량 배치 처리로 API 비용이 부담될 때.
- 현실: 32GB 램에서 30B급, 128GB에서 100B급이 상한. 프론티어 모델 대비 **에이전트형 장기 작업 성공률이 눈에 띄게 낮다.**
- 권장 조합: 민감 데이터는 로컬 모델로 **마스킹/추출**만 하고, 마스킹된 산출물로 클라우드 모델을 쓰는 2단 구성.

| 장점 | 단점 |
|---|---|
| 데이터가 절대 밖으로 안 나감 | 하드웨어 초기비용, 전력, 관리 부담 |
| 토큰 과금 없음, 무제한 반복 | 성능 격차(특히 멀티스텝 에이전트) |
| 오프라인 가능, 지연 낮음 | 모델 업데이트·양자화·서빙을 직접 관리 |
| 프라이버시 요구 규제 대응 | 긴 컨텍스트에서 메모리 벽 |

---

## 권장 조합 (개인 개발자 기준)

```
평상시 개발      : 로컬 CLI (빠른 피드백, 로컬 테스트)
큰 작업          : 로컬에서 plan → 커밋 → claude --cloud 로 실행 위임
이동 중          : 모바일 앱에서 클라우드 세션 확인·지시
결과 회수        : claude --teleport 로 로컬로 끌어와 마무리
협업/자동화      : GitHub PR 중심 (@claude, 자동 리뷰, Auto-fix)
민감 데이터      : 로컬 오픈웨이트 모델로 전처리
```

**하이브리드의 유일한 전제**: 상태는 대화가 아니라 **git과 파일**로 흘러야 한다.
계획서·결정사항·TODO를 커밋해두면 어느 환경에서든 이어받을 수 있고, 그러지 않으면 세션이 끊기는 순간 전부 증발한다.

## 참고
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)
- [Cloud environments](https://code.claude.com/docs/en/cloud-environments)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
