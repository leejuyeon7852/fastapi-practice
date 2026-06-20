# FastAPI Practice Backend

AndroidPractice (Kotlin/Compose) 앱의 백엔드 서버입니다.

## 기술 스택

- **FastAPI** — Python 웹 프레임워크
- **SQLAlchemy** — ORM
- **SQLite** (개발) → **PostgreSQL** (배포 예정)
- **Alembic** — DB 마이그레이션
- **JWT** — 인증 (HTTPBearer)

## 실행 방법

```bash
# 가상환경 활성화
source venv/Scripts/activate  # Windows (Git Bash)

# 서버 실행
uvicorn main:app --reload

# 마이그레이션
alembic upgrade head
```

## 프로젝트 구조

```
fastapi-practice/
├── main.py
├── alembic/
├── app/
│   ├── core/
│   │   ├── deps.py       # 인증 의존성
│   │   └── security.py   # JWT, 비밀번호 해싱
│   ├── models/           # SQLAlchemy 모델
│   ├── schemas/          # Pydantic 스키마
│   ├── crud/             # DB 조작 함수
│   ├── routers/          # API 엔드포인트
│   └── database.py
└── uploads/              # 업로드 이미지 저장
```

## API 문서

서버 실행 후 `http://localhost:8000/docs` 에서 Swagger UI로 확인
