feat(api): add IP-based rate limit middleware

Protect API endpoints from abuse by capping each client IP to
100 requests per 60-second window. Uses a fixed-window counter
kept in an in-memory Map, returning HTTP 429 once the limit is
exceeded and resetting the count when the window rolls over.

Refs: PROJ-481
