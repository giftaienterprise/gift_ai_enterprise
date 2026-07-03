# GitHub Actions Backend Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a GitHub Actions workflow that validates the Python 3.11 backend on every relevant pull request and push.

**Architecture:** A single least-privilege GitHub-hosted job checks out the repository, provisions Python 3.11 with pip caching, installs the pinned requirements, and runs the same dependency, compilation, and unittest checks used by the internal deployment. A repository hygiene test locks the workflow's triggers, runtime, permissions, commands, and test-only configuration in place.

**Tech Stack:** GitHub Actions, Ubuntu runner, Python 3.11, unittest, pip

---

### Task 1: Specify the CI workflow contract

**Files:**
- Modify: `backend/tests/test_project_hygiene.py`
- Test: `backend/tests/test_project_hygiene.py`

- [ ] **Step 1: Add a failing workflow contract test**

Add this method to `ProjectHygieneTests`:

```python
def test_backend_ci_matches_deployment_checks(self):
    workflow = (ROOT / ".github/workflows/backend-tests.yml").read_text()
    self.assertIn("pull_request:", workflow)
    self.assertIn("master", workflow)
    self.assertIn("codex/**", workflow)
    self.assertIn("permissions:\n  contents: read", workflow)
    self.assertIn("uses: actions/checkout@v6", workflow)
    self.assertIn("uses: actions/setup-python@v6", workflow)
    self.assertIn("python-version: '3.11'", workflow)
    self.assertIn("cache: pip", workflow)
    self.assertIn("python -m pip check", workflow)
    self.assertIn("python -m compileall -q app", workflow)
    self.assertIn(
        "python -m unittest discover -s tests -p 'test_*.py' -v",
        workflow,
    )
    self.assertIn("DATABASE_URL: sqlite:///./ci.db", workflow)
    self.assertIn("SECRET_KEY: ci-only-secret", workflow)
```

- [ ] **Step 2: Run the contract test and verify it fails**

Run from `backend`:

```powershell
..\.venv\Scripts\python.exe -m unittest tests.test_project_hygiene.ProjectHygieneTests.test_backend_ci_matches_deployment_checks -v
```

Expected: `ERROR` with `FileNotFoundError` for `.github/workflows/backend-tests.yml`.

- [ ] **Step 3: Commit the failing contract test together with the approved design and plan**

```powershell
git add backend/tests/test_project_hygiene.py docs/superpowers/specs/2026-07-03-github-actions-backend-tests-design.md docs/superpowers/plans/2026-07-03-github-actions-backend-tests.md
git commit -m "test: define backend CI contract"
```

### Task 2: Implement the backend CI workflow

**Files:**
- Create: `.github/workflows/backend-tests.yml`
- Test: `backend/tests/test_project_hygiene.py`

- [ ] **Step 1: Create the workflow**

Create `.github/workflows/backend-tests.yml` with:

```yaml
name: Backend tests

on:
  pull_request:
    branches:
      - master
  push:
    branches:
      - master
      - codex/**

permissions:
  contents: read

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    defaults:
      run:
        working-directory: backend
    env:
      DATABASE_URL: sqlite:///./ci.db
      SECRET_KEY: ci-only-secret
      DEBUG: "false"
      AI_CACHE_ENABLED: "false"
    steps:
      - name: Check out repository
        uses: actions/checkout@v6
      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: '3.11'
          cache: pip
          cache-dependency-path: requirements.txt
      - name: Install dependencies
        working-directory: .
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt
      - name: Check dependencies
        working-directory: .
        run: python -m pip check
      - name: Compile backend
        run: python -m compileall -q app
      - name: Run backend tests
        run: python -m unittest discover -s tests -p 'test_*.py' -v
```

- [ ] **Step 2: Run the focused contract test and verify it passes**

Run from `backend`:

```powershell
..\.venv\Scripts\python.exe -m unittest tests.test_project_hygiene.ProjectHygieneTests.test_backend_ci_matches_deployment_checks -v
```

Expected: one test, `OK`.

- [ ] **Step 3: Run the complete local verification**

Run from `backend`:

```powershell
..\.venv\Scripts\python.exe -m pip check
..\.venv\Scripts\python.exe -m compileall -q app tests
..\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py' -v
git -C .. diff --check
```

Expected: dependency check succeeds, compilation exits zero, 21 tests pass, and `git diff --check` exits zero.

- [ ] **Step 4: Commit the workflow**

```powershell
git add .github/workflows/backend-tests.yml
git commit -m "ci: add backend test workflow"
```

### Task 3: Publish and verify the first GitHub run

**Files:**
- No file changes

- [ ] **Step 1: Push the active branch**

```powershell
git -c http.proxy=http://127.0.0.1:7897 push origin codex/project-stability
```

Expected: the remote branch advances to the two new CI commits.

- [ ] **Step 2: Verify PR metadata and checks**

```powershell
$env:HTTP_PROXY='http://127.0.0.1:7897'
$env:HTTPS_PROXY='http://127.0.0.1:7897'
& 'C:\Program Files\GitHub CLI\gh.exe' pr checks 1 --repo giftaienterprise/gift_ai_enterprise --watch
```

Expected: the `Backend tests` check completes successfully.

- [ ] **Step 3: Verify final repository state**

```powershell
git status -sb
git log -2 --oneline
```

Expected: the working tree is clean and the branch matches `origin/codex/project-stability`.
