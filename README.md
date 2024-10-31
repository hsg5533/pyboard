# Simple Django Bulletin Board

이 프로젝트는 Django로 구현한 간단한 게시판 웹 애플리케이션입니다. 사용자가 게시글을 작성하고 수정 및 삭제할 수 있는 기본적인 CRUD 기능을 제공합니다.

## 주요 기능

- 게시글 작성
- 게시글 목록 보기
- 게시글 수정
- 게시글 삭제

## 요구사항

- Python 3.x
- Django 4.x 이상

## 설치 방법

1. 이 레포지토리를 클론합니다:

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. 가상환경을 생성하고 활성화합니다:

   ```bash
   python -m venv venv
   source venv/bin/activate  # 윈도우의 경우 venv\Scripts\activate
   ```

3. 필요한 패키지를 설치합니다:

   ```bash
   pip install -r requirements.txt
   ```

4. 데이터베이스 마이그레이션을 실행합니다:

   ```bash
   python manage.py migrate
   ```

5. 로컬 서버를 시작합니다:

   ```bash
   python manage.py runserver
   ```

6. 브라우저에서 `http://127.0.0.1:8000`로 이동하여 애플리케이션을 확인합니다.

## 폴더 구조

```
simple-django-bulletin-board/
├── board/                # 메인 애플리케이션 디렉토리
│   ├── migrations/       # 데이터베이스 마이그레이션 파일
│   ├── templates/        # HTML 템플릿 파일
│   ├── views.py          # 뷰 로직
│   ├── models.py         # 데이터베이스 모델 정의
│   └── urls.py           # URL 라우팅 설정
├── pyboard/              # Django 프로젝트 설정
│   ├── settings.py       # Django 설정 파일
│   └── urls.py           # 프로젝트 URL 라우팅
└── manage.py             # Django 관리 명령어
```

## 사용법

1. 게시글 작성:

   - 메인 페이지에서 "새 글 작성" 버튼을 클릭하여 제목과 내용을 입력하고 게시글을 생성합니다.

2. 게시글 수정 및 삭제:
   - 게시글 상세 페이지에서 "수정" 또는 "삭제" 버튼을 눌러 해당 작업을 수행할 수 있습니다.

## 기여 방법

- 이 프로젝트에 기여하고 싶다면 PR을 보내주세요!
