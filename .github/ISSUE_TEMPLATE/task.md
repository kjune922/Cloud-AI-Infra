목표

1. PostgreSQL 컨테이너 실행 -> Docker사용
2. SQLAlchemy 기본설정해봄 
3. TaskResult 모델 만들고 결과조회해봄
4. 테이블생성된거 확인했음

공부한것

쿼리 파라미터 공부 "POST"

Path parameter: URL 일부로 데이터 받음

Query parameter: ?key=value 형식으로 데이터 받음

POST + JSON Body: 구조화된 데이터 받음 (Pydantic으로 검증 가능)


- Celery는 비동기 작업 처리 (백그라운드 작업 큐)를 가능하게
해주는 툴

- Redis는 그 메세지 브로커역할을 함

오늘작업결과

docker exec -it pg psql -U kjune922 -d cloud_ai 로 
 Schema |     Name     | Type  |  Owner
--------+--------------+-------+----------
 public | task_results | table | kjune922
 이렇게 확인했음

 ------
 2025-09-23

1. FastAPI에 /webbook/ API추가
 -> 외부에서 JSON데이터를 POST형식으로 받음

2. 받은 데이터를 바로 처리하지 않고 -> Celery Task로 넘김
3. Celery Task가 PostgreSQL webhook_events 테이블에 저장
 
 4. celery log확인하는건 윈도우에서는 celery -A src.celery_app.celery_app worker --loglevel=info --pool=solo

------
2025.09.24
2025.09.24

이제 AWS하고 접합하는데

서버안에서 애플리케이션 실행/중지 방법
(Docker Compose)

<실행>

cd /app   # 프로젝트 위치
docker-compose up -d

<상태확인>
docker-compose ps

<실시간 FastAPI, Celery, Redis 로그 확인>
docker-compose logs -f

<중지>
docker-compose down

---------------------------
Docker Compose 기반 배포준비

목표는 FastAPI + Celery Worker + Redis를 한방에 띄우는
docker-compose.yml 만들기

!!! 끄고 키는법
docker-compose down -> 끈다

docker-compose up -d -> 킨다