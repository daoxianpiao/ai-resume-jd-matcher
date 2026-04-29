import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import main  # noqa: E402

RESUME = (
    "人工智能专业本科生，会 Python，了解机器学习，正在学习 FastAPI、Docker、"
    "OpenAI API 和 RAG。做过图像分类课程项目，希望求职 AI 应用开发工程师。"
)

JOB_DESCRIPTION = (
    "招聘 AI Native 应用开发工程师，要求熟悉 Python、FastAPI、OpenAI API、"
    "RAG、Docker，能完成基础前端页面和后端接口联调，有 AI 应用项目经验优先。"
)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DATABASE_PATH", tmp_path / "app.db")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    main.init_db()
    return TestClient(main.app)


def create_analysis(client: TestClient) -> dict:
    response = client.post(
        "/api/analyze",
        data={
            "resume": RESUME,
            "job_description": JOB_DESCRIPTION,
        },
    )
    assert response.status_code == 200
    return response.json()


def test_health(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_creates_history_and_learning_tasks(client: TestClient):
    payload = create_analysis(client)

    assert payload["analysis_mode"] == "demo"
    assert payload["analysis_id"] > 0
    assert payload["overall_score"] >= 0
    assert len(payload["learning_tasks"]) == len(payload["learning_plan_30_days"])

    history = client.get("/api/history").json()["items"]
    assert history[0]["id"] == payload["analysis_id"]
    assert history[0]["task_total"] == len(payload["learning_tasks"])
    assert history[0]["task_completed"] == 0


def test_patch_learning_task_updates_progress(client: TestClient):
    payload = create_analysis(client)
    task_id = payload["learning_tasks"][0]["id"]

    response = client.patch(
        f"/api/learning-tasks/{task_id}",
        json={"is_completed": True},
    )
    updated = response.json()

    assert response.status_code == 200
    assert updated["is_completed"] is True
    assert updated["completed_at"] is not None

    history = client.get("/api/history").json()["items"]
    assert history[0]["task_completed"] == 1


def test_extract_text_file(client: TestClient):
    response = client.post(
        "/api/extract-file",
        files={
            "file": (
                "resume.txt",
                RESUME.encode("utf-8"),
                "text/plain",
            )
        },
    )
    payload = response.json()

    assert response.status_code == 200
    assert payload["filename"] == "resume.txt"
    assert "FastAPI" in payload["text"]


def test_rejects_unsupported_file_type(client: TestClient):
    response = client.post(
        "/api/extract-file",
        files={
            "file": (
                "resume.exe",
                b"not allowed",
                "application/octet-stream",
            )
        },
    )

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]
