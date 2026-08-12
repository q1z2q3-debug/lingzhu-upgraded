# 🚀 lingzhu 快速部署指南

## 本地开发

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

```bash
# 复制环境配置示例
cp .env.example .env

# 编辑 .env 文件（可选，默认配置即可开发）
```

### 3. 启动服务

```bash
# 开发模式（自动重载）
uvicorn src.lingzhu.main:app --reload --port 8000

# 或生产模式
uvicorn src.lingzhu.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

---

## Docker 部署

### 1. 构建镜像

```bash
docker build -t lingzhu:latest .
```

### 2. 运行容器

```bash
docker run -d \
  --name lingzhu \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  -v lingzhu_data:/app/data \
  lingzhu:latest
```

### 3. 使用 Docker Compose

```bash
docker-compose up -d
```

---

## 生产环境部署

### 系统要求

- Python 3.10+
- 2GB+ RAM
- 10GB+ 存储空间

### Gunicorn + Uvicorn

```bash
gunicorn src.lingzhu.main:app \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --timeout 30 \
  --keep-alive 5
```

### Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name api.lingzhu.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 环境变量配置

```bash
# .env 生产环境配置
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://user:pass@localhost:5432/lingzhu
RATE_LIMIT_PER_MINUTE=100
```

---

## 数据库迁移

### 使用 Alembic (推荐)

```bash
# 安装 Alembic
pip install alembic

# 初始化
alembic init alembic

# 配置 alembic.ini
# 修改 sqlalchemy.url = sqlite+aiosqlite:///./lingzhu.db

# 创建迁移
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

---

## 监控与日志

### 健康检查

```bash
curl http://localhost:8000/health
```

### 查看日志

```bash
# 开发模式
tail -f lingzhu.log

# Docker
docker logs -f lingzhu
```

### 性能监控

- 使用 Prometheus + Grafana
- 集成 Sentry 错误追踪
- 使用 New Relic APM

---

## 备份与恢复

### 数据库备份

```bash
# SQLite 备份
cp lingzhu.db lingzhu.backup.$(date +%Y%m%d).db

# PostgreSQL 备份
pg_dump lingzhu > backup.sql
```

### 恢复数据库

```bash
# SQLite
cp lingzhu.backup.db lingzhu.db

# PostgreSQL
psql lingzhu < backup.sql
```

---

## 故障排查

### 常见问题

**1. 数据库锁定**
```bash
# 删除锁文件
rm lingzhu.db-journal
```

**2. 端口占用**
```bash
# 查找占用端口的进程
lsof -i :8000
# 杀死进程
kill -9 <PID>
```

**3. 依赖冲突**
```bash
# 清理并重装
pip cache purge
pip install -r requirements.txt --force-reinstall
```

---

## 安全建议

1. **生产环境务必修改默认 API 密钥前缀**
2. **启用 HTTPS** (Let's Encrypt 免费证书)
3. **配置防火墙** (只开放必要端口)
4. **定期更新依赖** (`pip list --outdated`)
5. **启用速率限制** (防止 DDoS)
6. **配置日志轮转** (防止磁盘爆满)

---

## 性能优化

### 数据库优化

```bash
# SQLite 优化
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA cache_size=10000;
```

### 应用优化

- 启用 Redis 缓存
- 使用数据库连接池
- 启用 Gzip 压缩
- 配置 CDN 静态资源

---

## 升级指南

```bash
# 拉取最新代码
git pull origin main

# 安装新依赖
pip install -r requirements.txt --upgrade

# 运行数据库迁移
alembic upgrade head

# 重启服务
systemctl restart lingzhu
```

---

## 支持

- 文档：https://github.com/q1z2q3-debug/lingzhu-upgraded
- Issues: https://github.com/q1z2q3-debug/lingzhu-upgraded/issues
- Email: lingzhu@runzeai-lab.com
