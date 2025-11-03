from sqlalchemy import Column, Integer, String, create_engine # --> column, integer, string은 실제 db 컬럼정의, create_engine() db연결엔진
from sqlalchemy.ext.declarative import declarative_base # declarative_base --> 모든 모델들이 상속할 "기본 베이스 클래스"생성
from sqlalchemy.orm import sessionmaker # -- db 세션관리 팩토리

# DB 접속정보 
DATABASE_URL = "postgresql+psycopg2://kjune922:dlrudalswns2@db:5432/cloud_ai"

# SQLALchemy 엔진 생성
engine = create_engine(DATABASE_URL) # -> DB와 실제 연결 통로

# 세션 (DB 연결관리)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 기본 모델 클래스는?

Base= declarative_base()

## TaskResult 모델 정의공간
# --> Celery 작업 결과를 저장할 테이블

class TaskResult(Base):
  __tablename__ = "task_results"
  
  id = Column(Integer,primary_key=True,index=True)
  task_id = Column(String,unique=True,index=True)
  status = Column(String)
  result = Column(String)
  
  ## Webhook정의구간
  
from sqlalchemy import Column, Integer, String, JSON, DateTime, func
  
class WebhookEvent(Base):
  __tablename__ = "webhook_events"
    
  id = Column(Integer,primary_key=True,index=True)
  event_type = Column(String,index=True) # 이벤트종류 정의
  payload = Column(JSON) # 전달된 데이터(JSON전체를 저장하겠음)
  create_at = Column(DateTime, server_default=func.now()) # 저장 시간정의