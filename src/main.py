from fastapi import FastAPI, Request
from celery.result import AsyncResult
from src.celery_app import celery_app, add, ask_llm, get_task_result
from src.db.models import SessionLocal, TaskResult, WebhookEvent

# FastAPI 앱 인스턴스 생성하는거임

app = FastAPI()

# 기본 라우트

#@app.get("/")
 #def read_root():
   #return {"message": "Hello Cloud-AI-Agent-Infra Project"}

@app.get("/hello/{name}")
def say_hello(name: str):
  return {"message": f"Hello,{name}"}

@app.get("/bye/{name}")
def say_bye(name:str):
  return {"message": f"GoodBye, {name}"}

@app.get("/next")
def say_next():
  return {
    "message" : "This is Next Page"
  }
  
### 혼자 추가로 라우팅공부

# Query Parameter (쿼리 스트링)

@app.get("/items")
def read_item(item_id: int, q: str = None):
  return {"item_id": item_id, "q": q}

## 클라이언트가 보내는 JSON 데이터를 받는 방법
# 이때 Pydantic 모델을 사용한다.

from pydantic import BaseModel

class Item(BaseModel):
  name: str
  price: float
  
@app.post("/items")
def create_item(item: Item):
  return {"name" : item.name, "price": item.price}

## FastAPI에서 Celery Task호출해보기

from src.celery_app import add, get_task_result


@app.get("/")
def read_root():
  return{
    "message": "Hello 이경준의 클라우드 인프라 프로젝트"
  }
  
@app.get("/add-task/")
def run_add_task(x: int, y:int):
  task = add.delay(x,y)
  return {
    "task_id":task.id
  }
  
@app.get("/task-result/{task_id}")
def check_task_result(task_id: str):
  return get_task_result(task_id) 

from src.db.models import SessionLocal,TaskResult # Task Rsult -> 우리가 SQLAlchemy로 정의한 모델 클래스(->DB테이블 task_reuslts에 매핑됨)

@app.get("/db-results/") # FaskAPI 엔드포인트 정의
def get_db_results(): # 요청이 들어오면 이 함수 실행
  db = SessionLocal() # DB 세션 객체 생성 -> 여기서 db는 실제로 PostgreSQL에 연결된 통로역할, 이걸로 insert, select, update 같은 sql실행 ㅇㅋ
  try: # DB연결을 열었으니 이제 할일을 try에, 닫을땐 finally로 안전하게 사용
    results = db.query(TaskResult).all() # -> select * from task_results 와 같은 말이다 그리고 ".all()"은 전체 행을 Python 객체 리스트로 가져온다는
    # 즉, results에는 TaskResult 객체들이 들어있다.
    response_data = []   # 최종 결과를 담을 리스트

    for r in results:    # results에 있는 TaskResult 객체들을 하나씩 꺼냄
      row = {          # 각 객체에서 필요한 값만 뽑아서 딕셔너리 생성
        "task_id": r.task_id,
        "status": r.status,
        "result": r.result
      }
      response_data.append(row)   # 리스트에 추가

    return response_data
  finally:  # 작업 끝나면 DB닫음
    db.close()

@app.post("/webhook")
async def receive_webhook(request:Request):
  data = await request.json()
  event_type = data.get("type","unknown")  # JSON에 "type"키가 없으면 unknown처리하겠음
  task = save_webhook_event.delay(event_type,data)
  return {
    "task_id" : task.id,
    "status" : "받았음"
  }
  
# webhook 저장라우트 선언


@app.get("/webhook-results/")
def get_webhook_results():
  db = SessionLocal()
  try:
    results = db.query(WebhookEvent).all()
    response_data = []
    for r in results:
      row = {
        "id":r.id,
        "event_type":r.event_type,
        "payload":r.payload
      }
      response_data.append(row)
    return response_data
  finally:
    db.close()
    


@app.post("/ask-llm/")
def run_llm(prompt: str):
  task = ask_llm.delay(prompt)
  return {"task_id":task.id}

