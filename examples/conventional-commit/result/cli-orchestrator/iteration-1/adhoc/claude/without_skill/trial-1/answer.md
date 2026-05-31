요청은 단순합니다 — 이 diff에 대한 커밋 메시지 작성. 글로벌 git-workflow 규칙(`<type>: <description>`, conventional commits)에 맞춰 작성합니다.

```
feat: add IP-based rate limiting middleware

Cap requests at 100 per 60s window per client IP; respond with HTTP 429
when the limit is exceeded. Hit counts are tracked in an in-memory Map
keyed by req.ip, with the window reset lazily on first request after expiry.

Refs: PROJ-481
```

타입 근거: 신규 동작(rate limiting)을 추가하므로 `feat`. 브랜치명의 `PROJ-481`을 `Refs:`로 연결했습니다.

참고로, 커밋 메시지와 별개로 코드에서 눈에 띄는 점 두 가지(원하시면 다음 작업으로):
- 인메모리 `Map`이라 다중 인스턴스 환경에선 인스턴스별로 카운트가 갈립니다(분산 환경이면 Redis 등 공유 저장소 필요). 또한 만료 항목이 정리되지 않아 IP가 누적되면 메모리 누수 소지가 있습니다.
- TS 파일인데 `rateLimit` 매개변수에 타입이 없습니다(`req: Request, res: Response, next: NextFunction`). import는 했지만 적용되지 않았습니다.

커밋 메시지만 필요하셨다면 위 블록을 그대로 쓰시면 됩니다.