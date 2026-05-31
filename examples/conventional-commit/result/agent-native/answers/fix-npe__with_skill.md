feat(profile): fall back to email for display name

The previous implementation dereferenced user.profile.nickname
directly, throwing a null-pointer error whenever profile or
nickname was missing. Use optional chaining and fall back to the
user's email so a missing nickname yields a safe, sensible label
instead of crashing.

Refs: PROJ-512
