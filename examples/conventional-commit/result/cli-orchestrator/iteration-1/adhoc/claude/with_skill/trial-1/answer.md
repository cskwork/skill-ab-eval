브랜치 `feature/PROJ-481-rate-limit`에서 티켓 ID `PROJ-481`을 추출했고, 신규 기능 추가이므로 `feat` 타입으로 작성했습니다.

```
feat(api): add request rate limiting middleware

Protect API endpoints from abuse by capping each client IP to 100
requests per minute. Requests exceeding the limit receive a 429
response so upstream resources stay available under bursty traffic.

Refs: PROJ-481
```

검증 내용:
- **Subject 길이**: `feat(api): add request rate limiting middleware` = 47자 (≤50 충족)
- **Imperative**: "add" 사용 (명령형)
- **Blank line**: subject와 body 사이 한 줄
- **Body 줄바꿈**: 모든 줄 72컬럼 이하, *why*(남용 방지/리소스 보호) 중심 서술
- **Refs 푸터**: `PROJ-481` 명시 (CI 필수 정책 충족)

참고: 디자인상 `hits` Map이 무한정 커질 수 있어(메모리 누수) 만료 엔트리 정리 로직이 없는 점, IP 키가 프록시 환경에서 신뢰 불가한 점은 후속 작업으로 검토할 가치가 있습니다. 다만 요청하신 건 커밋 메시지 작성이므로 위 메시지만 제공합니다.