# FastAPI Practice Backend

AndroidPractice 앱의 RoomDB 기반 기능을 FastAPI 백엔드로 옮기기 위한 연습용 프로젝트입니다.

## Collaboration Rules

- 사용자가 허락하기 전에는 기존 코드를 바로 편집하지 않습니다.
- 구현 전에 어떤 구조로 만들지 먼저 설명합니다.
- FastAPI를 처음 배우는 흐름에 맞춰 쉬운 단계부터 진행합니다.
- 한 번에 많은 기능을 만들기보다 작은 단위로 만들고 확인합니다.
- AndroidPractice의 RoomDB 구조는 참고하되, 백엔드는 서버 기준으로 다시 설계합니다.

## Learning Path

1. FastAPI 기본 앱 실행 이해
2. posts CRUD 구현
3. router, schema, model, crud 역할 분리 이해
4. SQLite로 로컬 DB 연습
5. users 추가
6. posts와 users 관계 연결
7. auth/login 구조 추가
8. comments, likes, scraps, follows, notifications 확장
9. Alembic 마이그레이션 도입
10. 배포 연습 단계에서 PostgreSQL 전환

## Initial Scope

처음 구현 범위는 posts CRUD입니다.

- `GET /posts`: 게시글 전체 조회
- `GET /posts/{post_id}`: 게시글 단건 조회
- `POST /posts`: 게시글 생성
- `PUT /posts/{post_id}`: 게시글 수정
- `DELETE /posts/{post_id}`: 게시글 삭제

## Post Field Draft

AndroidPractice의 `Post` 엔티티를 참고하되, Python/FastAPI 스타일의 snake_case를 사용합니다.

- `id`
- `author_id`
- `author_nickname`
- `title`
- `body`
- `image_uri`
- `created_at`

## Recommended Structure

```text
fastapi-practice/
├── main.py
├── requirements.txt
├── AGENTS.md
└── app/
    ├── __init__.py
    ├── database.py
    ├── models/
    │   ├── __init__.py
    │   └── post.py
    ├── schemas/
    │   ├── __init__.py
    │   └── post.py
    ├── crud/
    │   ├── __init__.py
    │   └── post.py
    └── routers/
        ├── __init__.py
        └── posts.py
```

## Database Plan

- 학습 초기에는 SQLite를 사용합니다.
- 배포 연습 단계에서는 PostgreSQL로 전환합니다.
- DB 연결 코드는 `app/database.py`에 모아 두어 나중에 DB를 바꾸기 쉽게 합니다.

## Style Notes

- 초보자가 읽기 쉬운 코드를 우선합니다.
- 복잡한 추상화는 처음부터 만들지 않습니다.
- 파일별 역할을 명확하게 나눕니다.
- 설명은 한국어로, 코드는 FastAPI/Python 관례에 맞춰 작성합니다.
