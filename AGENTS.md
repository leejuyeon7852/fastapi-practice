# FastAPI Practice Backend

AndroidPractice 앱의 RoomDB 기반 기능을 FastAPI 백엔드로 옮기기 위한 연습용 프로젝트입니다.

## Collaboration Rules

- 사용자가 허락하기 전에는 기존 코드를 바로 편집하지 않습니다.
- 구현 전에 어떤 구조로 만들지 먼저 설명합니다.
- FastAPI를 처음 배우는 흐름에 맞춰 쉬운 단계부터 진행합니다.
- 한 번에 많은 기능을 만들기보다 작은 단위로 만들고 확인합니다.
- AndroidPractice의 RoomDB 구조는 참고하되, 백엔드는 서버 기준으로 다시 설계합니다.

## Learning Path

1. FastAPI 기본 앱 실행 이해 ✅
2. posts CRUD 구현 ✅
3. router, schema, model, crud 역할 분리 이해 ✅
4. SQLite로 로컬 DB 연습 ✅
5. users 추가 ✅
6. posts와 users 관계 연결 ✅
7. auth/login 구조 추가 ✅
8. comments, likes, scraps, follows 확장 ✅
9. 마이페이지 / 검색 / 프로필 수정 ✅
10. Alembic 마이그레이션 도입 ✅
11. 안드로이드 연동
12. 배포 및 PostgreSQL 전환

## 구현된 API

### Posts
- `GET /posts` — 게시글 전체 조회
- `GET /posts/{post_id}` — 게시글 단건 조회
- `GET /posts/search?q=` — 게시글 검색
- `POST /posts` — 게시글 생성 (이미지 포함, 인증 필요)
- `PUT /posts/{post_id}` — 게시글 수정 (인증 필요)
- `DELETE /posts/{post_id}` — 게시글 삭제 (인증 필요)

### Users
- `POST /users/signup` — 회원가입
- `POST /users/login` — 로그인 (JWT 반환)
- `GET /users/me` — 내 정보 조회 (닉네임, 팔로워/팔로잉 수)
- `PUT /users/me` — 프로필 수정 (닉네임, 이미지)
- `GET /users/search?q=` — 유저 검색
- `GET /users/me/posts` — 내 게시글 목록
- `GET /users/me/comments` — 내 댓글 목록
- `GET /users/me/likes` — 내가 좋아요한 게시글
- `GET /users/me/scraps` — 내 스크랩 목록

### Comments
- `GET /posts/{post_id}/comments` — 댓글 목록
- `POST /posts/{post_id}/comments` — 댓글 작성 (인증 필요)
- `DELETE /comments/{comment_id}` — 댓글 삭제 (인증 필요)

### Likes
- `POST /posts/{post_id}/like` — 게시글 좋아요 토글 (인증 필요)
- `POST /comments/{comment_id}/like` — 댓글 좋아요 토글 (인증 필요)

### Scraps
- `POST /posts/{post_id}/scrap` — 스크랩 토글 (인증 필요)

### Follows
- `POST /users/{user_id}/follow` — 팔로우/언팔로우 토글 (인증 필요)
- `GET /users/me/followers` — 내 팔로워 목록
- `GET /users/me/following` — 내 팔로잉 목록

## TODO

- 안드로이드 연동 테스트
- 배포 (서버 선택 후)
- PostgreSQL 전환

## Style Notes

- 초보자가 읽기 쉬운 코드를 우선합니다.
- 복잡한 추상화는 처음부터 만들지 않습니다.
- 파일별 역할을 명확하게 나눕니다.
- 설명은 한국어로, 코드는 FastAPI/Python 관례에 맞춰 작성합니다.
