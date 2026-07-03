# API Security Hardening Design

## Goal

Harden the current FastAPI application for controlled production preparation
without changing database tables or existing business data. Authentication,
rate limits, upload validation, and error boundaries must be explicit and
covered by automated tests.

## Authentication Boundary

Use the existing signed JWT access token and `users` table. Add an OAuth2
Bearer dependency that decodes the token with the configured algorithm,
requires a valid numeric subject, loads the user from the current database
session, and rejects missing, expired, invalid, deleted, or inactive users with
HTTP 401. The dependency returns the active `User` for downstream identity and
rate-limit keys.

The following endpoints remain public:

- `/`, `/health`, `/api/auth/register`, and `/api/auth/login`;
- gift, brand, and category list/detail reads;
- static files already published below the upload URL prefix.

Authentication is required for:

- gift, brand, and category create/update/delete operations;
- gift image attach/delete and image upload;
- all `/ai/*` and `/agent/*` operations.

No administrator-only policy is introduced in this change. Existing users and
tokens remain compatible because the token subject already contains the user
ID.

## AI and Agent Rate Limit

Add a focused, thread-safe in-memory sliding-window limiter. Its key is the
authenticated user ID and its policy is 10 requests per rolling 60-second
window for all AI and Agent routes combined. A rejected request returns HTTP
429 and a stable `AI_RATE_LIMIT_EXCEEDED` detail. Old timestamps are discarded
on every check so idle users consume no lasting state.

The current deployment runs one Uvicorn worker, so process-local state matches
the deployment topology. The counter resets on restart and must be replaced by
a shared Redis limiter before running multiple workers or instances.

## Upload Validation

Accept only JPEG, PNG, and WebP images, with a maximum raw upload payload
of 5 MiB. Validation requires all of the following:

- an allowed request content type;
- a matching binary signature (JPEG SOI, PNG signature, or RIFF/WEBP markers);
- a total payload no greater than 5 MiB.

Read at most 5 MiB plus one byte, reject oversized or mismatched files with
HTTP 413 or 415, and write only validated bytes. Continue generating random
server-side filenames; derive the stored extension from the detected image
type rather than the untrusted client filename. SVG, GIF, executable content,
and extension-only validation are not allowed.

## Error Boundary and Logging

Provider, Agent, and upload failures must not return raw exception strings.
Log unexpected exceptions server-side with stack traces and return stable,
generic client details. Authentication failures use a consistent Bearer
challenge. Existing business validation and not-found responses remain intact.

## Components

- `app/core/security.py`: token decoding helper.
- `app/core/dependencies.py`: active-user Bearer dependency.
- `app/core/rate_limit.py`: thread-safe per-user AI limiter.
- API routers: dependency wiring and stable error handling.
- `app/services/storage/local_storage_service.py`: bounded reads, binary
  signature detection, safe extension selection, and validated writes.
- Tests: authentication matrix, inactive/deleted/expired tokens, shared AI
  limit, accepted image formats, spoofed/oversized uploads, and error
  redaction.

## Data and Deployment Compatibility

No schema migration is required. The current SQLite database, users, gifts,
uploads, and JWT signing secret remain in place. The Nginx 10 MiB request limit
stays as an outer transport ceiling; the application enforces the stricter
5 MiB policy.

## Acceptance Criteria

- All public endpoints remain accessible without a token.
- Every protected mutation, upload, AI, and Agent endpoint returns 401 without
  a valid active-user token.
- Valid active-user tokens preserve current successful behavior.
- The eleventh AI/Agent request in 60 seconds returns 429 for that user without
  affecting another user.
- Valid JPEG, PNG, and WebP payloads up to 5 MiB are accepted.
- Oversized, spoofed, GIF, SVG, and executable payloads are rejected without
  being written.
- Unexpected internal exception text is absent from client responses.
- The full local suite and GitHub Actions pass before deployment.
