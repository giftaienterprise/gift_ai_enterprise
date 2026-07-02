# Gift AI Enterprise 项目稳健治理报告

## 执行结果

- 工作分支：`codex/project-stability`
- Python：3.12
- 应用编译：通过
- 自动化测试：16/16 通过
- 健康检查：`GET /health` 返回 HTTP 200 与 `{"status":"healthy"}`
- 依赖一致性：`pip check` 无冲突

## 已修复问题

1. 新增统一 Windows 启动脚本，固定使用项目 `.venv` 和 `backend` 工作目录。
2. 完善 Git 忽略边界，覆盖虚拟环境、IDE 状态、Python/测试缓存、本地数据库、环境文件与上传目录。
3. 仅从 Git 索引取消跟踪 `.venv`、`.idea`、Python 缓存与上传内容；磁盘文件保留。
4. 删除根目录两个长度为零且无引用的 Python 占位文件；真实入口 `backend/app/main.py` 保留。
5. 恢复 `AIProviderRouter.register_provider()` 兼容接口。
6. 修复 `/ai/analyze-product` 将 `AIResponse` 再次嵌套导致响应字段丢失的问题。
7. 删除 AI 工具模块的导入时控制台输出。
8. 在 AI provider 边界验证返回类型，避免错误响应被宽泛异常静默吞掉。
9. 增加仓库卫生、导入副作用和 provider 边界回归测试。
10. 将 `requirements.txt` 从 UTF-16 LE 规范化为 UTF-8。
11. 恢复认证、分类、品牌、礼品、上传与礼品图片路由的 `/api` 注册，避免应用仅暴露 AI 功能。
12. 恢复礼品路由对 `gift_service` 单例的导入，避免列表、详情、更新与删除发生 `NameError`。
13. 新增主路由兼容测试，覆盖原 API 路径、礼品 CRUD 服务连接、根路径与健康接口。

## 已验证的兼容依赖升级

- Alembic：1.14.0 → 1.18.5
- SQLAlchemy：2.0.36 → 2.0.51
- PyMySQL：1.1.1 → 1.2.0
- Pydantic：2.10.3 → 2.13.4
- pydantic-core：2.27.1 → 2.46.4
- pydantic-settings：2.6.1 → 2.14.2
- python-dotenv：1.0.1 → 1.2.2
- python-jose：3.3.0 → 3.5.0
- python-multipart：0.0.17 → 0.0.32
- typing-extensions：4.15.0 → 4.16.0
- 新增 Pydantic 所需的 typing-inspection 0.4.2

以上版本先在独立临时虚拟环境完成安装、`pip check` 和 13 项测试，再同步到项目 `.venv`。

## 审计结论

- 事务上下文中的宽泛异常用于保证数据库回滚后原样抛出，属于合理边界。
- Redis 客户端捕获 `RedisError` 并降级返回，符合缓存不可用不阻断主业务的设计。
- JSON 解析器中的异常用于逐级容错；本轮保持其既有输出语义。
- AI provider 调用层将外部异常转换为失败响应，保持现有 API 稳定性。
- 跟踪文件中发现的是配置变量引用，没有发现被跟踪的真实 `.env` 或明文密钥文件。
- 测试目录中的打印仅存在于手工 Redis/缓存诊断脚本，不在确定性测试发现范围内。

## 暂缓项目

- FastAPI 0.139 会使 Starlette 从 0.41 跨至 1.x；按不跨主要版本的稳健规则，本轮保留 FastAPI 0.115.6、Starlette 0.41.3 和 Uvicorn 0.32.1。
- bcrypt 5、Redis 8 均为主要版本升级，本轮保留现有版本。
- pip 升级时留下 `.venv/Lib/site-packages/~qlalchemy` 与 `~ydantic_core` 临时目录，因 Windows 中仍有 Python 进程占用二进制文件而未强制删除。它们位于已忽略的虚拟环境内，不影响导入、测试或 Git。

## 文件删除与保留原则

- 已删除：根目录空的 `main.py`、`__init__.py`，理由是长度为零、无引用且会混淆真实入口。
- 已保留：两个数据库初始化入口、上传内容、本地数据库、虚拟环境和全部未提交业务源码。
- 未执行强制重置、历史重写或本地数据清理。

## 本地数据库与业务冒烟

- 使用现有 `Base.metadata.create_all()` 非破坏性创建缺失的 `categories`、`brands`、`gifts` 与 `gift_images` 表；已有 `users` 表和数据未删除。
- 只读请求 `/api/gifts/`、`/api/categories/`、`/api/brands/` 均返回 HTTP 200。
- `/api/auth/login` 与 `/api/upload/image` 在缺少必填请求体时均返回 HTTP 422，验证请求校验链正常。
- 根路径、健康检查与 OpenAPI 文档均返回 HTTP 200。
