# 项目学习笔记

这份笔记用来复习本项目的核心工程能力。重点不是背代码，而是理解一个 AI Web 应用从输入到输出的完整链路。

## 1. 请求链路

```text
浏览器表单
  -> fetch("/api/analyze")
  -> FastAPI 接收 resume 和 job_description
  -> demo 规则或 OpenAI Responses API 生成结构化结果
  -> SQLite 保存分析历史
  -> SQLite 创建学习任务
  -> 前端渲染分数、建议、任务看板
```

关键文件：

- `templates/index.html`：用户输入、按钮事件、fetch 请求、结果渲染
- `main.py`：API 路由、AI 分析逻辑、数据库读写

## 2. 核心接口

| 接口 | 方法 | 作用 |
| --- | --- | --- |
| `/health` | GET | 健康检查 |
| `/api/analyze` | POST | 提交简历和 JD，生成分析 |
| `/api/extract-file` | POST | 上传文件并提取文本 |
| `/api/history` | GET | 获取最近分析记录 |
| `/api/history/{analysis_id}` | GET | 获取某次分析详情 |
| `/api/learning-tasks/{task_id}` | PATCH | 更新任务完成状态 |
| `/api/learning-tasks/{task_id}` | DELETE | 删除学习任务 |

FastAPI 会自动生成 Swagger 文档：

```text
http://127.0.0.1:8001/docs
```

## 3. 结构化输出

AI 应用不应该只返回一段不可控文本。本项目用 `MatchAnalysis` 约束输出字段：

- `overall_score`
- `summary`
- `strengths`
- `risks`
- `score_breakdown`
- `missing_keywords`
- `learning_plan_30_days`
- `project_suggestions`
- `interview_talking_points`

这样前端可以稳定渲染，数据库可以稳定保存，测试也可以验证关键字段。

## 4. 数据库关系

项目使用两张 SQLite 表：

```text
analyses
  id
  created_at
  analysis_mode
  target_role
  overall_score
  resume
  job_description
  result_json

learning_tasks
  id
  analysis_id
  title
  position
  is_completed
  completed_at
```

关系：

```text
一次分析 analyses.id
  -> 多条学习任务 learning_tasks.analysis_id
```

这就是后端常见的一对多关系。

## 5. CRUD 闭环

本项目已经覆盖基础 CRUD：

- Create：`POST /api/analyze` 创建分析记录和学习任务
- Read：`GET /api/history`、`GET /api/history/{analysis_id}` 读取记录
- Update：`PATCH /api/learning-tasks/{task_id}` 更新任务状态
- Delete：`DELETE /api/learning-tasks/{task_id}` 删除任务

面试表达可以说：

> 我通过 FastAPI 设计 REST API，并使用 SQLite 完成分析历史和学习任务的一对多数据建模，支持创建、查询、更新、删除的完整 CRUD 闭环。

## 6. Docker 运行逻辑

`Dockerfile` 负责构建镜像：

```text
Python 基础镜像 -> 安装依赖 -> 复制代码 -> 启动 uvicorn
```

`compose.yaml` 负责运行服务：

```yaml
ports:
  - "${APP_PORT:-8001}:8000"
volumes:
  - ./data:/app/data
```

重点理解：

- 容器内部端口是 `8000`
- 电脑访问端口是 `8001`
- `./data:/app/data` 让 SQLite 数据不会因为容器重建而丢失

## 7. 测试和 CI

本地运行：

```powershell
pytest -q
ruff check .
```

GitHub Actions 会在每次 push 后自动执行：

```text
安装依赖 -> ruff check . -> pytest -q
```

这说明项目不仅能运行，还具备基本工程质量保障。

## 8. 面试讲解顺序

可以按这个顺序讲：

1. 我想解决的问题：AI 应用岗位求职时，快速分析简历和 JD 的匹配度。
2. 我怎么做：FastAPI 提供 API，前端用 fetch 调用，模型输出结构化 JSON。
3. 数据怎么保存：SQLite 保存分析历史和学习任务，形成一对多关系。
4. 如何交付：Docker Compose 一键运行，README 提供样例和截图。
5. 如何保证质量：pytest 覆盖核心接口，GitHub Actions 自动跑 CI。

## 9. 下一步学习

- 把 demo 分析升级为真实 OpenAI API 调用
- 做第二个项目：个人知识库 RAG 问答系统
- 学习部署：Render、Railway、Fly.io 或云服务器
- 学习更完整的前端框架：React 或 Next.js
