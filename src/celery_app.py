from celery import Celery

# Redis를 브로커로 사용하는 Celery 인스턴스 생성
celery_app = Celery(
  "Worker",
  broker = "redis://redis:6379/0",
  backend= "redis://redis:6379/0"
)


## Celery 작업 결과 확인 함수 만들어보쟈잉

from celery.result import AsyncResult


def get_task_result(task_id: str):
  result = AsyncResult(task_id, app=celery_app)
  return {
    "task_id": task_id,
    "status": result.status,
    "result": result.result
  }


## 이제는 celery_app.task의 작업이 끝나면 DB에 저장하도록 바꿔보자
from src.db.models import SessionLocal, TaskResult

@celery_app.task
def add(x,y):
  result_value = x + y
  
  # DB연결
  db = SessionLocal()
  try:
    task_result = TaskResult(
      task_id = add.request.id, # Celery가 생성한 고유 TaskID
      status = "성공입니다",
      result = str(result_value) 
    )
    db.add(task_result)
    db.commit()
  finally:
    db.close()
    
  return result_value

from src.db.models import SessionLocal, WebhookEvent
import json

@celery_app.task
def save_webhook_event(event_type: str, payload: dict):
  db = SessionLocal()
  try:
    event = WebhookEvent(
      event_type = event_type,
      payload = json.dumps(payload, ensure_ascii=False)
    )
    db.add(event)
    db.commit()
  finally:
    db.close()
  return {"status":"saved","event_type":event_type}


from src.db.models import TaskResult
import requests
OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_MODEL = "llama2" 


@celery_app.task
def ask_llm(prompt: str):
  # OpenAI API 호출을 하려했으나 과금이슈로
  # Ollama로 교체
  
  url = "http://127.0.0.1:11434/api/chat"
  payload = {
        "model": "llama2",   # ollama에 설치된 모델명 (예: llama2, gemma:2b, mistral 등)
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
  }
  resp = requests.post(url, json=payload)
  resp.raise_for_status()  # 오류 있으면 예외 발생
  data = resp.json()
  result_text = data["message"]["content"]
  # DB 저장
  db = SessionLocal()
  try:
    task_result = TaskResult(
      task_id = ask_llm.request.id, # Celery가 부여한 고유 ID
      status = "성공해씀",
      result = result_text
    )
    db.add(task_result)
    db.commit()
  finally:
    db.close()
  return result_text