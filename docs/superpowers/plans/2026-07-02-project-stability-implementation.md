# Gift AI Enterprise Stability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean the repository, restore the existing test contract, harden deterministic failure paths, and update compatible dependencies without changing public API behavior.

**Architecture:** Work in four checkpoints: repository/environment hygiene, regression repair, targeted stability hardening, then dependency verification. Preserve the current layered FastAPI structure and all user source changes; prefer compatibility methods and narrow fixes over broad rewrites.

**Tech Stack:** Python 3.12, FastAPI, Pydantic 2, SQLAlchemy 2, Redis, unittest, Uvicorn, PowerShell, Git.

---

## File responsibility map

- `.gitignore`: excludes local/runtime/generated artifacts from version control.
- `.env.example`: documents required configuration without secrets.
- `requirements.txt`: reproducible runtime dependency lock.
- `start_backend.ps1`: canonical Windows development startup.
- `backend/app/services/ai/provider_router.py`: provider registration and resolution.
- `backend/app/api/ai.py`: stable HTTP response envelopes for AI endpoints.
- `backend/app/services/ai/ai_facade.py`: prompt construction, provider dispatch, and typed output parsing.
- `backend/tests/test_ai_api.py`: public AI endpoint compatibility tests.
- `backend/tests/test_ai_facade_regressions.py`: AI facade and provider compatibility tests.
- `backend/tests/test_project_hygiene.py`: repository and import-side-effect regression checks.
- `docs/project-stability-report.md`: final audit evidence, deferred findings, and dependency decisions.

## Checkpoint 1: Repository and environment hygiene

### Task 1: Protect local artifacts and secrets

**Files:**
- Modify: `.gitignore`
- Create: `.env.example`
- Test: `backend/tests/test_project_hygiene.py`

- [ ] **Step 1: Write the failing ignore-policy test**

```python
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ProjectHygieneTests(unittest.TestCase):
    def test_local_artifacts_are_ignored(self):
        candidates = [
            ".venv/Scripts/python.exe",
            "backend/app/__pycache__/main.pyc",
            "backend/gift_ai.db",
            "backend/.env",
            "uploads/example.png",
            ".pytest_cache/state",
            ".ruff_cache/state",
        ]
        result = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            cwd=ROOT,
            input="\n".join(candidates),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(result.stdout.splitlines()), set(candidates))
```

- [ ] **Step 2: Run the test and verify it fails for uploads and tool caches**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_project_hygiene.ProjectHygieneTests.test_local_artifacts_are_ignored -v`

Expected: FAIL because the current `.gitignore` does not cover all candidates.

- [ ] **Step 3: Extend `.gitignore` with explicit runtime boundaries**

```gitignore
# Virtual environments
.venv/
venv/

# IDE-local state
.idea/

# Python caches and tooling
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.mypy_cache/
.coverage
htmlcov/

# Local databases and secrets
*.db
.env
.env.*
!.env.example

# Runtime uploads
uploads/
backend/uploads/
```

- [ ] **Step 4: Add a secret-free `.env.example`**

```dotenv
DATABASE_URL=sqlite:///./gift_ai.db
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEEPSEEK_API_KEY=
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
AI_CACHE_ENABLED=true
```

- [ ] **Step 5: Re-run the hygiene test**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_project_hygiene.ProjectHygieneTests.test_local_artifacts_are_ignored -v`

Expected: PASS.

### Task 2: Stop tracking generated files without deleting local copies

**Files:**
- Modify Git index only: `.venv/**`, `.idea/**`, `**/__pycache__/**`, `*.pyc`, `uploads/**`
- Preserve on disk: all matching paths

- [ ] **Step 1: Record before-state counts and local sentinel hashes**

Run:

```powershell
$tracked = git ls-files
($tracked | Where-Object { $_ -like '.venv/*' }).Count
Get-FileHash .venv\Scripts\python.exe
Get-ChildItem uploads -Recurse -File | Measure-Object
```

Expected: about 2182 tracked virtual-environment files, six tracked cache files, six tracked uploads, and local files present.

- [ ] **Step 2: Remove generated paths from the Git index only**

Run:

```powershell
git rm -r --cached --ignore-unmatch .venv .idea uploads backend/uploads
git ls-files | Where-Object { $_ -match '(^|/)__pycache__/|\.py[co]$' } | ForEach-Object { git rm --cached --ignore-unmatch -- $_ }
```

Expected: paths are staged as deletions in Git while local files remain on disk.

- [ ] **Step 3: Verify local copies remain and tracking noise is gone**

Run:

```powershell
Test-Path .venv\Scripts\python.exe
Test-Path uploads
git ls-files .venv uploads .idea
```

Expected: both `Test-Path` calls return `True`; `git ls-files` returns no generated paths.

### Task 3: Remove confirmed empty root Python stubs

**Files:**
- Delete: `main.py`
- Delete: `__init__.py`

- [ ] **Step 1: Prove the stubs are empty and unreferenced**

Run:

```powershell
(Get-Item main.py).Length
(Get-Item __init__.py).Length
rg -n "root\.main|from main|import main" . -g '*.py' -g '!.venv/**'
```

Expected: both lengths are zero and the reference search returns no application references.

- [ ] **Step 2: Delete only the two confirmed empty stubs**

Use `apply_patch` to delete `main.py` and `__init__.py`. Do not delete either `backend/init_db.py` or `backend/app/database/init_db.py`; they have distinct CLI and package roles.

- [ ] **Step 3: Verify the real application entry remains importable**

Run: `cd backend; ..\.venv\Scripts\python.exe -c "from app.main import app; print(app.title)"`

Expected: `Gift AI Enterprise`.

## Checkpoint 2: Restore current behavior contracts

### Task 4: Restore provider registration compatibility

**Files:**
- Modify: `backend/app/services/ai/provider_router.py`
- Test: `backend/tests/test_ai_facade_regressions.py`

- [ ] **Step 1: Run the existing failing regression test**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_ai_facade_regressions.AIFacadeTests.test_builds_string_prompt_and_preserves_system_prompt -v`

Expected: ERROR with `AttributeError: 'AIProviderRouter' object has no attribute 'register_provider'`.

- [ ] **Step 2: Add the smallest typed registration method**

```python
from app.services.ai.providers.base import BaseAIProvider


def register_provider(self, provider: BaseAIProvider) -> None:
    if not provider.provider_name:
        raise ValueError("provider_name must not be empty")
    self.providers[provider.provider_name] = provider
```

Place the method on `AIProviderRouter`; retain default-provider fallback behavior.

- [ ] **Step 3: Run the targeted regression test**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_ai_facade_regressions.AIFacadeTests.test_builds_string_prompt_and_preserves_system_prompt -v`

Expected: PASS.

### Task 5: Preserve the analyze-product response envelope

**Files:**
- Modify: `backend/app/api/ai.py`
- Test: `backend/tests/test_ai_api.py`

- [ ] **Step 1: Run the existing failing API contract test**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_ai_api.AIAPITests.test_analyze_product_route -v`

Expected: ERROR with `KeyError: 'title'` because the route nests the `AIResponse` object instead of its data.

- [ ] **Step 2: Reuse the common response helper**

Replace the hand-built dictionary at the end of `analyze_product` with:

```python
return response("AI 商品统一分析成功", result)
```

- [ ] **Step 3: Run all API compatibility tests**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_ai_api -v`

Expected: all six API tests PASS.

### Task 6: Establish the clean regression baseline

**Files:**
- No production changes unless a newly exposed failure has a separately documented root cause.

- [ ] **Step 1: Compile all application modules**

Run: `.\.venv\Scripts\python.exe -m compileall -q backend\app`

Expected: exit code 0.

- [ ] **Step 2: Run the complete deterministic suite from the correct working directory**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py' -v`

Expected: all deterministic tests PASS. External Redis diagnostic scripts must not be counted as passing unit tests unless converted to isolated tests.

## Checkpoint 3: Targeted stability hardening

### Task 7: Remove import-time console output from the tool package

**Files:**
- Modify: `backend/app/services/ai/tools/init.py`
- Test: `backend/tests/test_project_hygiene.py`

- [ ] **Step 1: Add a failing import-side-effect test**

```python
def test_tool_package_import_is_silent(self):
    result = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "-c", "import app.services.ai.tools.init"],
        cwd=ROOT / "backend",
        text=True,
        capture_output=True,
        check=False,
    )
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout, "")
```

- [ ] **Step 2: Verify the test fails with `[ToolSystem] Loaded tools:` output**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_project_hygiene.ProjectHygieneTests.test_tool_package_import_is_silent -v`

Expected: FAIL because the module prints during import.

- [ ] **Step 3: Remove only the import-time `print` statement**

Keep `tool_registry` import and `__all__`; delete the debug `print` block. Do not change tool discovery behavior.

- [ ] **Step 4: Re-run the test**

Expected: PASS with empty stdout.

### Task 8: Make output parsing failures explicit but compatible

**Files:**
- Modify: `backend/app/services/ai/ai_facade.py`
- Test: `backend/tests/test_ai_facade_regressions.py`

- [ ] **Step 1: Add regression tests for dictionary data and invalid provider payloads**

Add a provider fixture returning `data={"text": "ok"}` and assert it is returned unchanged. Add a provider fixture returning an object without `data` and assert the facade raises a clear `TypeError` rather than silently swallowing it.

- [ ] **Step 2: Run the two tests and verify the invalid-payload test fails unclearly**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_ai_facade_regressions.AIFacadeTests -v`

Expected: the valid dictionary case passes; the invalid-payload contract fails before hardening.

- [ ] **Step 3: Narrow exception handling around optional typed parsing**

Use `isinstance(result, AIResponse)` to validate the provider boundary. Catch `pydantic.ValidationError` only when converting parsed text into `ProductAIResult`; preserve parsed dictionaries as the existing fallback. Remove the outer blanket `except Exception: pass`.

- [ ] **Step 4: Run facade and API tests**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest tests.test_ai_facade_regressions tests.test_ai_api -v`

Expected: all tests PASS with unchanged successful API envelopes.

### Task 9: Produce a bounded static audit report

**Files:**
- Create: `docs/project-stability-report.md`
- Modify production files only for high-confidence findings with a failing regression test.

- [ ] **Step 1: Run source checks**

Run:

```powershell
rg -n "except Exception|except:\s*$|pass\s*$|print\(" backend -g '*.py' -g '!**/__pycache__/**'
.\.venv\Scripts\python.exe -m compileall -q backend\app
git diff --check
```

- [ ] **Step 2: Classify every match**

Record file, line, behavior, risk, and disposition in `docs/project-stability-report.md`. Abstract base-class `pass` statements are valid; resilience boundaries that intentionally degrade Redis failures are valid; silent broad catches in core logic require a test-backed fix.

- [ ] **Step 3: Check secrets without printing values**

Run a name-only scan for `API_KEY`, `SECRET_KEY`, `PASSWORD`, and token assignments across tracked files. Record only file paths and variable names; never copy secret values into logs or the report.

- [ ] **Step 4: Re-run the full deterministic suite after each accepted finding**

Run: `cd backend; ..\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py' -v`

Expected: all tests remain PASS.

## Checkpoint 4: Compatible dependency update and final verification

### Task 10: Audit runtime dependencies before changing versions

**Files:**
- Modify: `requirements.txt`
- Update: `docs/project-stability-report.md`

- [ ] **Step 1: Capture installed and pinned versions**

Run:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip list --outdated
```

Expected: `pip check` reports no broken requirements; outdated packages are recorded without upgrading yet.

- [ ] **Step 2: Separate direct runtime dependencies from transitive packages**

Keep exact pins in `requirements.txt` for reproducibility, but update only packages whose compatibility is confirmed against FastAPI, Pydantic, SQLAlchemy, Redis, OpenAI-compatible clients, and Python 3.12. Do not cross a major version in this plan.

- [ ] **Step 3: Upgrade one dependency family at a time**

Families: web stack (`fastapi`, `starlette`, `uvicorn`, `httpx`), data stack (`SQLAlchemy`, `alembic`, `PyMySQL`), configuration/security, Redis, then AI client. After each family, run `pip check`, full tests, import check, and health check. If a family fails, restore only that family's prior pins and document the incompatibility.

- [ ] **Step 4: Freeze the verified environment**

Run: `.\.venv\Scripts\python.exe -m pip freeze --all`

Update `requirements.txt` only with the verified resolved versions; do not include editable local paths.

### Task 11: Verify from a clean temporary environment

**Files:**
- No source changes.

- [ ] **Step 1: Create a temporary verification environment outside the project `.venv`**

Run:

```powershell
python -m venv $env:TEMP\gift-ai-verify
& $env:TEMP\gift-ai-verify\Scripts\python.exe -m pip install -r requirements.txt
```

- [ ] **Step 2: Run compile, import, and deterministic tests in the clean environment**

Run:

```powershell
& $env:TEMP\gift-ai-verify\Scripts\python.exe -m compileall -q backend\app
Push-Location backend
& $env:TEMP\gift-ai-verify\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py' -v
Pop-Location
```

Expected: compile succeeds and all deterministic tests PASS.

- [ ] **Step 3: Start the app and verify health**

Start `app.main:app` from `backend` on an unused local port, poll `/health`, require HTTP 200 with `{"status":"healthy"}`, then terminate the verification process cleanly.

- [ ] **Step 4: Record final evidence**

Update `docs/project-stability-report.md` with test count, compile result, health result, dependency decisions, files removed or moved with reasons, and deferred items.

### Task 12: Final scope and Git review

**Files:**
- Review all changed files; make no new behavior changes.

- [ ] **Step 1: Confirm user source changes were preserved**

Run `git status --short`, `git diff --stat`, and targeted diffs for every modified source file. Confirm no unrelated user edit was overwritten.

- [ ] **Step 2: Confirm generated files are local but untracked**

Run `Test-Path .venv\Scripts\python.exe`, `Test-Path uploads`, and `git ls-files .venv uploads .idea`.

Expected: local checks are true and the Git query is empty.

- [ ] **Step 3: Run the final verification gate**

Run compileall, complete unittest discovery, `pip check`, secret-name scan, `git diff --check`, and `/health` verification fresh in this task.

Expected: no new failures, no tracked secrets, no whitespace errors, and healthy application startup.
