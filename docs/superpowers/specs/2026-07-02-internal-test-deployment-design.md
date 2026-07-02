# Gift AI Enterprise 内部测试部署设计

## 目标

将当前稳定分支部署到一台阿里云 ECS，供受控内部人员测试。服务器规格为 2 vCPU、2 GiB 内存、40 GiB ESSD Entry，操作系统为 Alibaba Cloud Linux 3.2104 LTS 64 位。

## 架构

外部测试请求只进入 Nginx 的 80 端口。Nginx 将请求转发到仅监听 `127.0.0.1:8000` 的 Uvicorn。应用由 systemd 以非 root 用户 `giftai` 运行，代码位于 `/opt/gift_ai_enterprise`，虚拟环境位于项目目录 `.venv`，运行数据保存在 `backend/gift_ai.db` 与 `uploads/`。

## 资源策略

- 创建 2 GiB Swap，降低依赖安装或短时峰值触发 OOM 的风险。
- Uvicorn 仅使用 1 个 worker。
- 内部测试继续使用 SQLite；不在同一台 2 GiB 服务器上运行高负载 Redis。
- 日志由 systemd journal 管理，Nginx 使用系统日志轮转。
- 云盘使用率达到 80% 时告警，并配置每日快照、保留 7 天。

## 网络与安全

- 安全组入方向仅开放 TCP 22 和 TCP 80，来源限定为管理员或内部测试人员公网 IP。
- TCP 8000、3306、5432、6379 不对外开放。
- SSH 优先使用密钥认证；不把私钥、密码或生产密钥写入仓库。
- 服务器 `.env` 权限设置为 `600`，由 `giftai` 读取。
- `DEBUG=false`，使用独立随机 `SECRET_KEY`。
- Nginx 限制请求体大小；应用上传目录仅授予 `giftai` 写权限。

## 部署流程

1. 验证 ECS 系统、CPU、内存、磁盘和安全组。
2. 安装 Git、Python 3、编译依赖与 Nginx。
3. 创建 `giftai` 系统用户、应用目录和 2 GiB Swap。
4. 从 GitHub 获取 `codex/project-stability` 用于内部测试；PR 合并后切换为 `master`。
5. 创建虚拟环境并安装 `requirements.txt`。
6. 在服务器交互式创建 `.env`，不通过聊天或 Git 传输密钥。
7. 非破坏性初始化 SQLite 表并执行自动化测试。
8. 安装 systemd 服务和 Nginx 站点配置。
9. 启动服务，验证本机与受控公网健康接口、OpenAPI 和只读业务接口。

## 数据与回滚

- 首次内部测试允许创建全新 SQLite 数据库。
- 后续部署前备份 `backend/gift_ai.db` 与 `uploads/`。
- 代码回滚使用上一已验证 Git 提交；数据库只在结构不兼容且备份可恢复时重建。
- systemd 启动失败时保持 Nginx 503，不把 Uvicorn 直接暴露到公网。

## 验收标准

- `systemctl is-active gift-ai` 返回 `active`。
- `nginx -t` 通过。
- 服务器本机 `http://127.0.0.1:8000/health` 返回 HTTP 200。
- 授权测试 IP 访问 `http://服务器IP/health` 返回 HTTP 200。
- 未开放端口 8000、数据库端口和 Redis 端口。
- 自动化测试全部通过，`pip check` 无依赖冲突。
- 重启服务器后应用与 Nginx 自动恢复。
