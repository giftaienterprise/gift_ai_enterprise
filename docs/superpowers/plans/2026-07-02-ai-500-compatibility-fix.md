# AI 500 Compatibility Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate confirmed AI endpoint 500 errors while preserving the existing public API and the in-progress facade/provider architecture.

**Architecture:** Keep `PromptManager` as the single prompt-construction boundary and make the facade translate request context into its established keyword-based contract. Providers receive separate user and system prompts through request metadata, while API routes delegate to `AIBusinessService` and expose consistent response envelopes.

**Tech Stack:** Python 3.12, FastAPI, Pydantic 2, built-in `unittest`, Starlette `TestClient`.

---

### Task 1: Pin the prompt and facade regressions

**Files:**
- Create: `backend/tests/test_ai_facade_regressions.py`
- Test: `backend/app/services/ai/prompts/product_description.py`
- Test: `backend/app/services/ai/ai_facade.py`

- [ ] **Step 1: Write failing tests** covering dictionary serialization, keyword mapping from facade context, and separate system/user prompts.
- [ ] **Step 2: Run tests to verify failure**

Run: `..\.venv\Scripts\python.exe -m unittest tests.test_ai_facade_regressions -v`

Expected: failures proving the current `dict.__dict__`, `ProductContext` positional argument, and tuple-as-prompt defects.

- [ ] **Step 3: Implement minimal contract fixes**

Serialize the product dictionary directly, map `category_name`/`brand_name` explicitly, and store the system prompt in `AIRequest.context["system_prompt"]` while keeping `AIRequest.prompt` a string.

- [ ] **Step 4: Run tests to verify they pass**

Run: `..\.venv\Scripts\python.exe -m unittest tests.test_ai_facade_regressions -v`

Expected: all facade regression tests pass.

### Task 2: Restore compatible AI API routes

**Files:**
- Modify: `backend/app/api/ai.py`
- Modify: `backend/app/services/business/ai_business_service.py`
- Modify: `backend/app/services/ai/providers/deepseek_provider.py`
- Test: `backend/tests/test_ai_api.py`

- [ ] **Step 1: Write failing API tests** for `/ai/product-description`, `/ai/product-tags`, `/ai/image-recognition`, `/ai/analyze-product`, and `/ai/test`, replacing the provider call with a deterministic local fake.
- [ ] **Step 2: Run tests to verify failure**

Run: `..\.venv\Scripts\python.exe -m unittest tests.test_ai_api -v`

Expected: missing routes or response-contract failures.

- [ ] **Step 3: Implement minimal route and service repairs**

Use typed Pydantic request bodies, delegate every route through `AIBusinessService`, pass `system_prompt` to DeepSeek, and make aggregate analysis tolerate optional image results while using the existing `ResultMerger` signature.

- [ ] **Step 4: Run tests to verify they pass**

Run: `..\.venv\Scripts\python.exe -m unittest tests.test_ai_api -v`

Expected: every endpoint returns a successful compatible envelope without external network access.

### Task 3: Remove confirmed broken references and verify application health

**Files:**
- Modify: `backend/app/services/business/gift_business_service.py`
- Test: `backend/tests/test_ai_facade_regressions.py`
- Test: `backend/tests/test_ai_api.py`

- [ ] **Step 1: Add import and service smoke tests** that instantiate the app and exercise all repaired service entrypoints.
- [ ] **Step 2: Run the smoke tests and confirm any remaining failure**.
- [ ] **Step 3: Replace stale `gift_ai_service` references with the repaired business/facade boundary, without unrelated refactoring**.
- [ ] **Step 4: Run full verification**

Run: `..\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v`

Run: `..\.venv\Scripts\python.exe -m compileall -q app tests`

Expected: tests pass, compilation succeeds, and application import lists all five AI routes.
