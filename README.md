# AI Resume JD Matcher

这是第一个 AI Native 应用开发练习项目：输入简历和岗位 JD，调用 OpenAI Responses API，返回结构化的岗位匹配分析。

## 你会学到什么

- 用 FastAPI 写一个最小后端服务
- 用普通 HTML/CSS/JavaScript 做一个够用的页面
- 用 OpenAI Python SDK 调用 Responses API
- 用 Pydantic 定义结构化输出
- 把 AI 输出转换成前端可渲染的数据
- 从 `.txt`、`.md`、`.pdf`、`.docx` 文件中抽取文本
- 用 SQLite 完成分析历史的新增、查询、删除和清空

## 运行方式

### 本地运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

然后编辑 `.env`。如果没有 OpenAI API Key，可以先保持默认值，项目会使用本地演示模式。

```powershell
uvicorn main:app --reload
```

打开：

```text
http://127.0.0.1:8000
```

### Docker 运行

需要先安装 Docker Desktop。

```powershell
docker compose up --build
```

Compose 默认把容器的 `8000` 端口映射到本机 `8001`，避免和本地开发服务冲突。

```text
http://127.0.0.1:8001
```

如果想改端口：

```powershell
$env:APP_PORT=8002
docker compose up --build
```

停止服务：

```powershell
docker compose down
```

## 运行测试

开发环境安装测试依赖：

```powershell
pip install -r requirements-dev.txt
```

运行接口测试：

```powershell
pytest -q
```

测试覆盖健康检查、简历分析、历史记录、学习任务状态更新、文件解析和非法文件拦截。

## 简历项目描述

基于 FastAPI + OpenAI Responses API 开发 AI 简历 JD 匹配助手，支持简历与岗位 JD 文本分析、文件解析、匹配度评分、能力短板识别、30 天学习计划生成、学习任务追踪、Markdown 报告导出和历史记录管理。项目使用 Pydantic 定义结构化结果，并通过 SQLite 实现分析历史和学习任务的新增、查询、更新、删除；使用 Dockerfile 和 Docker Compose 完成容器化部署，提升前后端数据解析稳定性、业务闭环完整度和交付可复现性。

## 当前功能

- 粘贴简历和岗位 JD 后生成匹配分析
- 没有 OpenAI API Key 时使用本地演示模式，方便继续学习前后端流程
- 上传 `.txt`、`.md`、`.pdf`、`.docx` 文件并自动填充文本
- 返回匹配度评分、能力拆分、关键词缺口、项目建议和面试表达要点
- 将当前分析结果导出为 Markdown 求职报告
- 自动保存分析历史，支持查看最近记录、点击回看、删除单条和清空全部
- 自动把 30 天学习计划拆成可勾选任务，并保存完成状态
- 支持 Dockerfile 和 Docker Compose 容器化运行
- 提供 `/health` 健康检查接口
