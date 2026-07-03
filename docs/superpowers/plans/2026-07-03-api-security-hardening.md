# API Security Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce active-user JWT authentication on sensitive endpoints, rate-limit AI calls, validate uploaded image bytes, and prevent raw internal errors from reaching clients.

**Architecture:** Reuse the existing JWT and user table through one FastAPI Bearer dependency. Keep rate limiting and upload validation in focused core/storage components, then wire them into routers declaratively. Preserve public reads and existing database data while locking every new boundary with unit and API tests.

**Tech Stack:** FastAPI, python-jose, SQLAlchemy, Python threading primitives, unittest, GitHub Actions

---

### Task 1: Active-user Bearer authentication

**Files:**
- Modify: `backend/app/core/security.py`
- Modify: `backend/app/core/dependencies.py`
- Create: `backend/tests/test_auth_security.py`

- [ ] **Step 1: Write failing dependency tests**

Create tests that patch `jwt.decode`, supply a mocked SQLAlchemy session, and assert: a valid active user is returned; missing user, inactive user, non-numeric subject, expired token, and invalid token all raise HTTP 401 with `WWW-Authenticate: Bearer`.

```python
class AuthenticationDependencyTests(unittest.TestCase):
    def test_returns_active_user(self):
        user = Mock(id=7, is_active=True)
        db = Mock()
        db.get.return_value = user
        with patch("app.core.security.jwt.decode", return_value={"sub": "7"}):
            self.assertIs(get_current_user("token", db), user)

    def test_rejects_inactive_user(self):
        db = Mock()
        db.get.return_value = Mock(id=7, is_active=False)
        with patch("app.core.security.jwt.decode", return_value={"sub": "7"}):
            with self.assertRaises(HTTPException) as raised:
                get_current_user("token", db)
        self.assertEqual(raised.exception.status_code, 401)
        self.assertEqual(raised.exception.headers["WWW-Authenticate"], "Bearer")
```

- [ ] **Step 2: Run the new module and verify RED**

Run from `backend`:

```powershell
..\.venv\Scripts\python.exe -m unittest tests.test_auth_security -v
```

Expected: import failure because `get_current_user` and `decode_access_token` do not exist.

- [ ] **Step 3: Add token decoding and the dependency**

Add to `security.py`:

```python
def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject.isdigit():
        raise JWTError("Invalid token subject")
    return subject
```

Add to `dependencies.py`:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        user_id = int(decode_access_token(token))
    except (JWTError, ValueError) as exc:
        raise credentials_exception() from exc
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_exception()
    return user
```

`credentials_exception()` returns HTTP 401, detail `INVALID_AUTHENTICATION`, and the Bearer challenge header.

- [ ] **Step 4: Run auth tests and the full suite**

Expected: auth tests and the existing 21 tests pass.

- [ ] **Step 5: Commit**

```powershell
git add backend/app/core/security.py backend/app/core/dependencies.py backend/tests/test_auth_security.py
git commit -m "feat: add active-user JWT dependency"
```

### Task 2: Protect sensitive route boundaries

**Files:**
- Modify: `backend/app/api/brand.py`
- Modify: `backend/app/api/category.py`
- Modify: `backend/app/api/gift.py`
- Modify: `backend/app/api/gift_image.py`
- Modify: `backend/app/api/upload.py`
- Modify: `backend/app/api/ai.py`
- Modify: `backend/app/api/agent.py`
- Create: `backend/tests/test_route_security.py`

- [ ] **Step 1: Write a failing route-security matrix**

Use `TestClient(app)` and assert unauthenticated requests return 401 for every mutation route, `/api/upload/image`, `/ai/test`, all AI POST routes, and `/agent/run`. Assert `/`, `/health`, register/login, and GET list/detail route metadata do not declare the Bearer dependency.

```python
PROTECTED = {
    ("POST", "/api/brands/"), ("PUT", "/api/brands/{brand_id}"),
    ("DELETE", "/api/brands/{brand_id}"),
    ("POST", "/api/categories/"), ("PUT", "/api/categories/{category_id}"),
    ("DELETE", "/api/categories/{category_id}"),
    ("POST", "/api/gifts/"), ("PUT", "/api/gifts/{gift_id}"),
    ("DELETE", "/api/gifts/{gift_id}"),
    ("POST", "/api/gifts/{gift_id}/images"),
    ("DELETE", "/api/gift-images/{image_id}"),
    ("POST", "/api/upload/image"),
}
```

Inspect each matching `APIRoute.dependant.dependencies` for `get_current_user`; perform real requests for `/ai/test` and `/agent/run` and expect 401.

- [ ] **Step 2: Run the matrix and verify RED**

Expected: protected dependency assertions fail and AI/Agent return a non-401 response.

- [ ] **Step 3: Wire authentication into routers**

For CRUD mutations, add decorator dependencies without changing handler signatures:

```python
@router.post("/", response_model=BrandResponse, dependencies=[Depends(get_current_user)])
```

Apply the same pattern to every route in `PROTECTED`. Add router-level authentication to AI and Agent temporarily:

```python
router = APIRouter(
    prefix="/ai",
    tags=["AI"],
    dependencies=[Depends(get_current_user)],
)
```

- [ ] **Step 4: Run route-security and full tests**

Update existing AI API tests to override `get_current_user` with an active test user so successful behavior remains covered. Expected: the security matrix and complete suite pass.

- [ ] **Step 5: Commit**

```powershell
git add backend/app/api backend/tests/test_route_security.py backend/tests/test_ai_api.py
git commit -m "feat: protect sensitive API routes"
```

### Task 3: Per-user AI sliding-window limit

**Files:**
- Create: `backend/app/core/rate_limit.py`
- Modify: `backend/app/core/dependencies.py`
- Modify: `backend/app/api/ai.py`
- Modify: `backend/app/api/agent.py`
- Create: `backend/tests/test_rate_limit.py`

- [ ] **Step 1: Write deterministic failing limiter tests**

Inject a fake monotonic clock. Assert requests 1-10 for one user are allowed, request 11 is denied, another user is unaffected, and advancing beyond 60 seconds restores access.

```python
clock = Mock(return_value=100.0)
limiter = SlidingWindowRateLimiter(limit=10, window_seconds=60, clock=clock)
for _ in range(10):
    self.assertTrue(limiter.allow("7"))
self.assertFalse(limiter.allow("7"))
self.assertTrue(limiter.allow("8"))
clock.return_value = 161.0
self.assertTrue(limiter.allow("7"))
```

- [ ] **Step 2: Verify RED**

Expected: module import failure.

- [ ] **Step 3: Implement the locked sliding window**

Use `dict[str, deque[float]]`, `threading.Lock`, and `time.monotonic`. Remove timestamps `<= now - window_seconds`, reject when the remaining deque length is at least the limit, otherwise append `now`.

Add:

```python
def enforce_ai_rate_limit(
    current_user: User = Depends(get_current_user),
) -> User:
    if not ai_rate_limiter.allow(str(current_user.id)):
        raise HTTPException(status_code=429, detail="AI_RATE_LIMIT_EXCEEDED")
    return current_user
```

Replace AI/Agent router dependency `get_current_user` with `enforce_ai_rate_limit` so one dependency performs both authentication and the shared limit.

- [ ] **Step 4: Verify limiter, route, and full tests**

Expected: deterministic limiter tests pass; the eleventh authenticated AI/Agent request returns 429; full suite passes.

- [ ] **Step 5: Commit**

```powershell
git add backend/app/core/rate_limit.py backend/app/core/dependencies.py backend/app/api/ai.py backend/app/api/agent.py backend/tests/test_rate_limit.py
git commit -m "feat: rate limit AI routes per user"
```

### Task 4: Validate uploaded image bytes

**Files:**
- Modify: `backend/app/core/config.py`
- Modify: `backend/app/services/storage/local_storage_service.py`
- Modify: `backend/app/api/upload.py`
- Create: `backend/tests/test_upload_security.py`

- [ ] **Step 1: Write failing storage tests**

Use a temporary upload directory and `UploadFile` backed by `BytesIO`. Cover a minimal JPEG header, PNG signature, WebP RIFF header, MIME/signature mismatch, GIF, SVG, executable bytes, and 5 MiB plus one byte. Assert rejected payloads create no files.

```python
JPEG = b"\xff\xd8\xff" + b"safe"
PNG = b"\x89PNG\r\n\x1a\n" + b"safe"
WEBP = b"RIFF\x04\x00\x00\x00WEBP" + b"safe"
```

- [ ] **Step 2: Verify RED**

Expected: spoofed and disallowed data are currently written or `STORAGE_DRIVER` access fails.

- [ ] **Step 3: Implement bounded validation**

Add `STORAGE_DRIVER: str = "local"` to settings. In local storage define `MAX_IMAGE_BYTES = 5 * 1024 * 1024`, allowed MIME/signature rules, `UnsupportedImageError`, and `UploadTooLargeError`. Read `MAX_IMAGE_BYTES + 1`, validate type and signature, select `.jpg`, `.png`, or `.webp` from detected bytes, and write validated bytes only.

Map expected exceptions in `upload.py`:

```python
except UploadTooLargeError as exc:
    raise HTTPException(status_code=413, detail="IMAGE_TOO_LARGE") from exc
except UnsupportedImageError as exc:
    raise HTTPException(status_code=415, detail="UNSUPPORTED_IMAGE_TYPE") from exc
```

- [ ] **Step 4: Verify upload and full tests**

Expected: accepted formats use server-selected extensions, all rejected payloads leave the directory empty, and the full suite passes.

- [ ] **Step 5: Commit**

```powershell
git add backend/app/core/config.py backend/app/services/storage/local_storage_service.py backend/app/api/upload.py backend/tests/test_upload_security.py
git commit -m "feat: validate uploaded image content"
```

### Task 5: Redact AI and Agent failures

**Files:**
- Modify: `backend/app/api/agent.py`
- Modify: `backend/app/services/ai/deepseek_ai_service.py`
- Modify: `backend/app/services/ai/providers/deepseek_provider.py`
- Create: `backend/tests/test_error_redaction.py`

- [ ] **Step 1: Write failing redaction tests**

Patch Agent and DeepSeek calls to raise `RuntimeError("secret path /opt/private")`. Assert logs capture the exception while API/provider results contain only `AGENT_EXECUTION_FAILED` or `AI_PROVIDER_ERROR`, never `secret`, `/opt/private`, API keys, or exception class text.

- [ ] **Step 2: Verify RED**

Expected: current responses expose the raw exception string.

- [ ] **Step 3: Add stable error boundaries**

Use module loggers and `logger.exception(...)`. Agent returns `error="AGENT_EXECUTION_FAILED"`. `DeepSeekAIService.chat` logs and raises `RuntimeError("DeepSeek request failed")` without embedding the upstream exception in returned JSON. `DeepSeekProvider.execute` catches unexpected exceptions, logs them, and returns `AIResponse(error="AI_PROVIDER_ERROR", success=False, ...)`.

- [ ] **Step 4: Verify redaction and full tests**

Expected: redaction tests and the complete suite pass with no raw exception in client-facing values.

- [ ] **Step 5: Commit**

```powershell
git add backend/app/api/agent.py backend/app/services/ai/deepseek_ai_service.py backend/app/services/ai/providers/deepseek_provider.py backend/tests/test_error_redaction.py
git commit -m "fix: redact internal AI errors"
```

### Task 6: Final verification and publication

**Files:**
- No file changes

- [ ] **Step 1: Run the complete verification gate**

Run from `backend`:

```powershell
..\.venv\Scripts\python.exe -m pip check
..\.venv\Scripts\python.exe -m compileall -q app tests
..\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py' -v
git -C .. diff --check
```

Expected: dependency and compilation checks succeed, every test passes, and no whitespace errors are reported.

- [ ] **Step 2: Review the complete diff against the specification**

Confirm every protected route declares the correct dependency; public reads remain public; no secret values or raw exception strings were added; no database schema or migration changed.

- [ ] **Step 3: Push the branch and open a new PR**

```powershell
git -c http.proxy=http://127.0.0.1:7897 push -u origin codex/api-security-hardening
```

Create a ready-for-review PR into `master` titled `feat: harden API security boundaries`, including the verification output and noting that deployment is not automatic.

- [ ] **Step 4: Wait for GitHub Actions**

```powershell
$env:HTTP_PROXY='http://127.0.0.1:7897'
$env:HTTPS_PROXY='http://127.0.0.1:7897'
& 'C:\Program Files\GitHub CLI\gh.exe' pr checks --repo giftaienterprise/gift_ai_enterprise --watch
```

Expected: `backend-tests` succeeds before any merge or deployment decision.
