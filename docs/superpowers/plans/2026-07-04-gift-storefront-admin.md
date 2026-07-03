# AI Gift Storefront and Admin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a responsive Vue storefront and Vue admin console on top of the existing FastAPI API, including AI gift guidance, product discovery, favorites/comparison, sharing, contact purchase, administrator-only writes, and configurable public contact/share settings.

**Architecture:** Keep `frontend/` and `admin/` as independent Vue 3 + Vite applications. Extend FastAPI with an administrator dependency and a singleton site-settings resource; public reads remain anonymous while every content mutation requires an administrator. Browser-local favorites and recommendation-share payloads keep the first release small and avoid adding an account subsystem.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy, unittest/pytest, Vue 3, TypeScript, Vite, Vue Router, Vitest, Testing Library, native Fetch API, Web Share API, QR code rendering.

---

### Task 1: Enforce administrator-only content mutations

**Files:**
- Modify: `backend/app/core/dependencies.py`
- Modify: `backend/app/api/gift.py`
- Modify: `backend/app/api/category.py`
- Modify: `backend/app/api/brand.py`
- Modify: `backend/app/api/upload.py`
- Modify: `backend/app/api/gift_image.py`
- Test: `backend/tests/test_admin_security.py`
- Test: `backend/tests/test_route_security.py`

- [ ] **Step 1: Write failing administrator dependency tests**

```python
from unittest.mock import Mock
from fastapi import HTTPException
from app.core.dependencies import require_admin

def test_require_admin_returns_admin():
    admin = Mock(is_admin=True, is_active=True)
    assert require_admin(admin) is admin

def test_require_admin_rejects_regular_user():
    try:
        require_admin(Mock(is_admin=False, is_active=True))
    except HTTPException as exc:
        assert exc.status_code == 403
        assert exc.detail == "ADMIN_REQUIRED"
    else:
        raise AssertionError("regular user was accepted")
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `cd backend; ..\.venv\Scripts\python.exe -m pytest tests/test_admin_security.py -q`

Expected: FAIL because `require_admin` is missing.

- [ ] **Step 3: Implement the dependency and replace write-route guards**

```python
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="ADMIN_REQUIRED")
    return current_user
```

Replace `Depends(get_current_user)` with `Depends(require_admin)` only on create, update, delete, attach-image, and upload routes. Keep public list/detail routes anonymous.

- [ ] **Step 4: Run security tests**

Run: `cd backend; ..\.venv\Scripts\python.exe -m pytest tests/test_admin_security.py tests/test_route_security.py tests/test_auth_security.py -q`

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```powershell
git add backend/app/core/dependencies.py backend/app/api backend/tests/test_admin_security.py backend/tests/test_route_security.py
git commit -m "feat: require admin for catalog mutations"
```

### Task 2: Add public contact and share settings

**Files:**
- Create: `backend/app/models/site_setting.py`
- Create: `backend/app/schemas/site_setting.py`
- Create: `backend/app/services/site_setting_service.py`
- Create: `backend/app/api/site_setting.py`
- Modify: `backend/app/models/__init__.py`
- Modify: `backend/app/database/init_db.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_site_settings.py`

- [ ] **Step 1: Write failing API contract tests**

```python
def test_public_settings_hide_internal_fields(client):
    response = client.get("/api/settings/public")
    assert response.status_code == 200
    assert set(response.json()["data"]) == {
        "wechat_id", "wechat_qr_url", "phone", "share_title",
        "share_description", "share_image_url",
    }

def test_regular_user_cannot_update_settings(client, user_headers):
    response = client.put("/api/settings", headers=user_headers, json={"phone": "10086"})
    assert response.status_code == 403
```

- [ ] **Step 2: Run and verify missing routes**

Run: `cd backend; ..\.venv\Scripts\python.exe -m pytest tests/test_site_settings.py -q`

Expected: FAIL with 404 responses.

- [ ] **Step 3: Implement singleton settings model and endpoints**

```python
class SiteSetting(Base):
    __tablename__ = "site_settings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    wechat_id: Mapped[str] = mapped_column(String(100), default="")
    wechat_qr_url: Mapped[str] = mapped_column(String(500), default="")
    phone: Mapped[str] = mapped_column(String(30), default="")
    share_title: Mapped[str] = mapped_column(String(150), default="AI送礼参谋")
    share_description: Mapped[str] = mapped_column(String(500), default="发现更贴心的礼物")
    share_image_url: Mapped[str] = mapped_column(String(500), default="")
```

Expose `GET /api/settings/public` anonymously, `GET /api/settings` to admins, and `PUT /api/settings` to admins. The service must create row `id=1` when absent.

- [ ] **Step 4: Run settings and route tests**

Run: `cd backend; ..\.venv\Scripts\python.exe -m pytest tests/test_site_settings.py tests/test_main_routes.py -q`

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```powershell
git add backend/app backend/tests/test_site_settings.py backend/tests/test_main_routes.py
git commit -m "feat: add public contact and share settings"
```

### Task 3: Add admin session endpoint and dashboard summary

**Files:**
- Modify: `backend/app/api/auth.py`
- Create: `backend/app/api/admin.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_admin_api.py`

- [ ] **Step 1: Write failing endpoint tests**

```python
def test_auth_me_returns_current_user(client, user_headers):
    response = client.get("/api/auth/me", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "member"

def test_admin_summary_requires_admin(client, user_headers):
    assert client.get("/api/admin/summary", headers=user_headers).status_code == 403
```

- [ ] **Step 2: Run and verify missing routes**

Run: `cd backend; ..\.venv\Scripts\python.exe -m pytest tests/test_admin_api.py -q`

Expected: FAIL with 404 responses.

- [ ] **Step 3: Implement endpoints**

`GET /api/auth/me` returns `UserResponse`. `GET /api/admin/summary` returns `gift_count`, `active_gift_count`, `category_count`, `brand_count`, and five recently updated gifts; it depends on `require_admin`.

- [ ] **Step 4: Run tests**

Run: `cd backend; ..\.venv\Scripts\python.exe -m pytest tests/test_admin_api.py tests/test_main_routes.py -q`

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```powershell
git add backend/app/api backend/app/main.py backend/tests
git commit -m "feat: add admin session and dashboard APIs"
```

### Task 4: Scaffold the storefront with tested shared API primitives

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/index.html`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/router.ts`
- Create: `frontend/src/styles/tokens.css`
- Create: `frontend/src/styles/global.css`
- Create: `frontend/src/api/http.ts`
- Create: `frontend/src/api/catalog.ts`
- Create: `frontend/src/types/catalog.ts`
- Create: `frontend/src/api/http.test.ts`

- [ ] **Step 1: Define scripts and dependencies**

Use Vue 3, Vue Router, Lucide Vue Next, `qrcode`, Vite, TypeScript, Vitest, jsdom, and Vue Testing Library. Scripts: `dev`, `build`, `test`, `test:run`.

- [ ] **Step 2: Write failing response-unwrapping tests**

```ts
it('unwraps the backend success envelope', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(
    JSON.stringify({ code: 200, message: 'success', data: { id: 1 } }),
    { status: 200, headers: { 'Content-Type': 'application/json' } },
  )))
  await expect(apiRequest<{ id: number }>('/gifts/1')).resolves.toEqual({ id: 1 })
})
```

- [ ] **Step 3: Implement `apiRequest`**

The helper prefixes `/api`, unwraps `{code,message,data}`, preserves FastAPI direct response models, adds bearer auth when supplied, and throws `ApiError(status, message)` for non-2xx responses.

- [ ] **Step 4: Install and run tests**

Run: `cd frontend; npm.cmd install; npm.cmd run test:run`

Expected: tests PASS.

- [ ] **Step 5: Commit**

```powershell
git add frontend
git commit -m "feat: scaffold Vue storefront"
```

### Task 5: Build the responsive storefront shell and catalog

**Files:**
- Create: `frontend/src/components/AppHeader.vue`
- Create: `frontend/src/components/BottomNav.vue`
- Create: `frontend/src/components/ProductCard.vue`
- Create: `frontend/src/views/HomeView.vue`
- Create: `frontend/src/views/CatalogView.vue`
- Create: `frontend/src/views/ProductView.vue`
- Create: `frontend/src/views/SavedView.vue`
- Create: `frontend/src/stores/favorites.ts`
- Test: `frontend/src/views/HomeView.test.ts`
- Test: `frontend/src/components/ProductCard.test.ts`

- [ ] **Step 1: Write failing UI tests**

Verify the home heading is `今天想为谁准备心意？`, catalog cards expose name and price, inactive products are not rendered, and the mobile navigation contains 首页、咨询、清单、我的.

- [ ] **Step 2: Run and verify failure**

Run: `cd frontend; npm.cmd run test:run`

Expected: FAIL because views and components are missing.

- [ ] **Step 3: Implement selected visual direction**

Use CSS variables `--coral: #ff625f`, `--orange: #ff874d`, `--ink: #20242c`, `--muted: #747984`, `--surface: #fff`, and radii from 16px to 28px. Match the selected 390×844 conversational design: assistant greeting, relationship/occasion/budget choices, gift preview, and fixed mobile navigation. At 960px, switch to a two-column layout without a phone frame.

- [ ] **Step 4: Implement product browsing and local favorites**

Fetch public categories, brands, gifts, and gift details. Persist favorite IDs under `gift-ai:favorites:v1`. Saved view renders favorites and lets the user select up to four products for comparison.

- [ ] **Step 5: Run tests and production build**

Run: `cd frontend; npm.cmd run test:run; npm.cmd run build`

Expected: tests PASS and `dist/` builds successfully.

- [ ] **Step 6: Commit**

```powershell
git add frontend
git commit -m "feat: build responsive gift catalog"
```

### Task 6: Implement AI advisor, contact purchase, and sharing

**Files:**
- Create: `frontend/src/views/AdvisorView.vue`
- Create: `frontend/src/components/ContactSheet.vue`
- Create: `frontend/src/components/ShareSheet.vue`
- Create: `frontend/src/composables/useShare.ts`
- Create: `frontend/src/api/advisor.ts`
- Modify: `frontend/src/views/ProductView.vue`
- Modify: `frontend/src/router.ts`
- Test: `frontend/src/composables/useShare.test.ts`
- Test: `frontend/src/views/AdvisorView.test.ts`

- [ ] **Step 1: Write failing interaction tests**

Test selection of relationship, occasion, and budget; verify the generated goal contains all selections; verify sharing uses `navigator.share` when available and clipboard fallback otherwise; verify missing phone or WeChat values hide their buttons.

- [ ] **Step 2: Run and verify failure**

Run: `cd frontend; npm.cmd run test:run`

Expected: FAIL because advisor and share modules are missing.

- [ ] **Step 3: Implement advisor data flow**

Post `{goal, use_brain: true}` to `/agent/run` with the logged-in token when available. If the existing endpoint requires authentication and the visitor is anonymous, show catalog-based recommendations immediately and present sign-in as optional rather than blocking ordinary browsing.

- [ ] **Step 4: Implement contact and sharing**

Load `/settings/public`; build `tel:` links; display the configured QR image and copyable WeChat ID. Share product or recommendation title, text, and stable URL through Web Share, then clipboard. Desktop share sheet renders a QR code for the current URL.

- [ ] **Step 5: Run tests and build**

Run: `cd frontend; npm.cmd run test:run; npm.cmd run build`

Expected: tests PASS and build succeeds.

- [ ] **Step 6: Commit**

```powershell
git add frontend
git commit -m "feat: add AI advisor contact and sharing"
```

### Task 7: Scaffold the administrator application

**Files:**
- Create: `admin/package.json`
- Create: `admin/vite.config.ts`
- Create: `admin/tsconfig.json`
- Create: `admin/index.html`
- Create: `admin/src/main.ts`
- Create: `admin/src/App.vue`
- Create: `admin/src/router.ts`
- Create: `admin/src/api/http.ts`
- Create: `admin/src/stores/auth.ts`
- Create: `admin/src/views/LoginView.vue`
- Create: `admin/src/layouts/AdminLayout.vue`
- Create: `admin/src/styles.css`
- Test: `admin/src/stores/auth.test.ts`

- [ ] **Step 1: Write failing authentication tests**

Verify login stores the token, calls `/auth/me`, rejects a non-admin response, and clears state on 401.

- [ ] **Step 2: Run and verify failure**

Run: `cd admin; npm.cmd install; npm.cmd run test:run`

Expected: FAIL because auth store is missing.

- [ ] **Step 3: Implement login and protected routes**

Use session storage key `gift-ai:admin-token`. The route guard waits for `auth.restore()`, redirects guests to `/login`, and redirects authenticated non-admin users to a 403 state. Never treat token presence alone as administrator proof.

- [ ] **Step 4: Build responsive admin shell**

Desktop uses left navigation; mobile uses a compact drawer. Reuse coral/orange tokens but prioritize dense readable tables and forms.

- [ ] **Step 5: Run tests and build**

Run: `cd admin; npm.cmd run test:run; npm.cmd run build`

Expected: tests PASS and build succeeds.

- [ ] **Step 6: Commit**

```powershell
git add admin
git commit -m "feat: scaffold secure admin console"
```

### Task 8: Build dashboard and catalog CRUD

**Files:**
- Create: `admin/src/views/DashboardView.vue`
- Create: `admin/src/views/ProductsView.vue`
- Create: `admin/src/views/ProductEditorView.vue`
- Create: `admin/src/views/CategoriesView.vue`
- Create: `admin/src/views/BrandsView.vue`
- Create: `admin/src/components/DataTable.vue`
- Create: `admin/src/components/ImageUploader.vue`
- Create: `admin/src/api/admin.ts`
- Test: `admin/src/views/ProductEditorView.test.ts`

- [ ] **Step 1: Write failing form tests**

Verify required product fields, integer-cent price payloads, upload progress state, cover assignment, save errors, and delete confirmation.

- [ ] **Step 2: Run and verify failure**

Run: `cd admin; npm.cmd run test:run`

Expected: FAIL because CRUD views are missing.

- [ ] **Step 3: Implement dashboard and product CRUD**

Use `/admin/summary`, `/gifts/`, `/upload/image`, and `/gifts/{id}/images`. Convert displayed yuan to integer cents before writes and cents back to yuan for display. Refresh the list only after confirmed successful mutations.

- [ ] **Step 4: Implement category and brand CRUD**

Support create, edit, sort, activate/deactivate, and confirmed delete. Show backend association errors without discarding form input.

- [ ] **Step 5: Run tests and build**

Run: `cd admin; npm.cmd run test:run; npm.cmd run build`

Expected: tests PASS and build succeeds.

- [ ] **Step 6: Commit**

```powershell
git add admin
git commit -m "feat: add admin catalog management"
```

### Task 9: Build contact and share settings administration

**Files:**
- Create: `admin/src/views/SettingsView.vue`
- Modify: `admin/src/api/admin.ts`
- Modify: `admin/src/router.ts`
- Test: `admin/src/views/SettingsView.test.ts`

- [ ] **Step 1: Write failing settings tests**

Verify loading existing values, phone validation, QR upload assignment, save payload, successful feedback, and retained values on server failure.

- [ ] **Step 2: Run and verify failure**

Run: `cd admin; npm.cmd run test:run`

Expected: FAIL because settings view is missing.

- [ ] **Step 3: Implement settings editor**

Fields are `wechat_id`, `wechat_qr_url`, `phone`, `share_title`, `share_description`, and `share_image_url`. Use the authenticated upload route for QR/default images and `PUT /settings` for persistence.

- [ ] **Step 4: Run tests and build**

Run: `cd admin; npm.cmd run test:run; npm.cmd run build`

Expected: tests PASS and build succeeds.

- [ ] **Step 5: Commit**

```powershell
git add admin
git commit -m "feat: manage contact and share settings"
```

### Task 10: Integrate deployment and verify the complete system

**Files:**
- Modify: `deploy/nginx/gift-ai.conf`
- Modify: `deploy/scripts/deploy_internal.sh`
- Modify: `deploy/README.md`
- Modify: `.gitignore`
- Test: `backend/tests/test_project_hygiene.py`

- [ ] **Step 1: Write failing deployment/hygiene assertions**

Assert the Nginx config serves storefront assets at `/`, admin assets at `/admin/`, preserves SPA fallbacks, proxies `/api/`, and serves `/uploads/` without exposing port 8000.

- [ ] **Step 2: Run and verify failure**

Run: `cd backend; ..\.venv\Scripts\python.exe -m pytest tests/test_project_hygiene.py -q`

Expected: FAIL until deployment files include both frontend builds.

- [ ] **Step 3: Update build and Nginx deployment**

The deployment script installs dependencies with `npm ci`, builds both applications, copies immutable assets to versioned release directories, initializes new SQLAlchemy tables, and reloads Nginx only after `nginx -t` succeeds.

- [ ] **Step 4: Run complete automated verification**

Run:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
cd ..\frontend
npm.cmd run test:run
npm.cmd run build
cd ..\admin
npm.cmd run test:run
npm.cmd run build
```

Expected: all backend and frontend tests PASS; both production builds succeed.

- [ ] **Step 5: Run Chrome visual and interaction QA**

Start the backend and both Vite previews. In Google Chrome, capture 390×844, 768px, and 1440×1024 views. Compare the 390×844 home/advisor state side by side with the selected visual image. Verify advisor choices, catalog/detail, favorite/compare, phone, WeChat, native-share fallback, admin login guard, product edit/upload, and settings persistence.

- [ ] **Step 6: Commit**

```powershell
git add deploy .gitignore backend/tests/test_project_hygiene.py
git commit -m "feat: deploy storefront and admin applications"
```
