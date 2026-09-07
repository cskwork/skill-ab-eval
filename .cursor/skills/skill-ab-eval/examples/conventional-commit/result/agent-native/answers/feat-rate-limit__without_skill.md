feat: add IP-based rate limiting middleware

Add fixed-window rate limiter to cap requests at 100 per minute per IP.
Returns HTTP 429 when the limit is exceeded.

Refs PROJ-481
