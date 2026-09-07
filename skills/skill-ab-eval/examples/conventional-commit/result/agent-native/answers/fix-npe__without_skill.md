fix: prevent NPE in displayName when profile or nickname is missing

Use optional chaining on profile/nickname and fall back to the user's
email when either is absent, instead of throwing on null access.

PROJ-512
