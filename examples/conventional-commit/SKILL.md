---
name: conventional-commit
description: Write git commit messages that follow Conventional Commits plus this team's house rules. Use when writing or...
---


# Conventional Commit (house style)

Write every commit message exactly like this:

```
<type>(<scope>): <subject>

<body>

Refs: <TICKET-ID>
```

Rules:

1. **Type** is one of: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`.
2. **Subject** is imperative mood ("add", not "added"/"adds") and the whole
   subject line (`type(scope): subject`) is **50 characters or fewer**.
3. Leave exactly **one blank line** between the subject and the body.
4. **Body** explains the *why*, wrapped at 72 columns.
5. **Always** end with a `Refs:` footer citing the ticket ID. If a branch name or
   context contains an ID like `PROJ-481`, use it. Never omit this footer.

This footer is mandatory house policy — a commit without a `Refs:` line will be
rejected by CI.
