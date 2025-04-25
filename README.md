# Janotion

Notion 스타일의 프로젝트/작업 관리 Django 웹서비스

## 주요 특징

- **프로젝트/작업 관리**: 칸반 보드, 테이블, 타임라인, 리스트 뷰 제공
- **드래그 앤 드롭**: 프로젝트 상태 변경 지원
- **Gantt(간트) 차트**: 프로젝트 일정 시각화
- **반응형 UI**: 데스크탑/모바일 모두 지원
- **로그인 없이 누구나 열람 가능**
- **세련된 Notion 스타일 디자인**

## 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/RJ-Stony/Janotion.git
cd Janotion
```

### 2. 가상환경 생성 및 활성화 (권장)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. DB 마이그레이션 (최초 1회)

```bash
python manage.py migrate
```

### 5. 서버 실행

```bash
python manage.py runserver
```

### 6. 접속

브라우저에서 [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 접속

---

## 개발/운영 참고

- **DB 파일(`db.sqlite3`)**: 버전에 따라 포함될 수 있습니다. 새로 시작하려면 삭제 후 migrate 하세요.
- **관리자 계정 생성** (필요시):
  ```bash
  python manage.py createsuperuser
  ```
- **정적 파일**: 개발환경에서는 자동 제공, 운영환경에서는 `python manage.py collectstatic` 필요

---

## 주요 기술스택

- Python 3.12+
- Django 4.2
- crispy-bootstrap5
- Pillow
- SQLite (기본)

---

## 기타

- 이 프로젝트는 Notion의 UI/UX에서 영감을 받았습니다.
- 문의/이슈는 [GitHub Issues](https://github.com/RJ-Stony/Janotion/issues)로 남겨주세요.

---
