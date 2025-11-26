# 🧮 Flask + FastAPI + PostgreSQL Calculator  
### (Basic Calculator + Scientific Calculator + Base Number Converter)

이 프로젝트는 **Flask 웹 UI**, **FastAPI 백엔드 API**, 그리고 **PostgreSQL 데이터베이스**를 기반으로 한  
웹 계산기 애플리케이션입니다.  
일반 계산기, 공학 계산기, 진수 변환 계산기를 통합해 하나의 웹에서 사용할 수 있습니다.

---

## 🚀 주요 기능

### ✔ 1. 일반 계산기 (Basic Calculator)
- 사칙연산(`+`, `-`, `*`, `/`)  
- 괄호 계산 지원  
- 직접 구현한 파서로 계산 수행  
- FastAPI 서버로 결과 전송하여 DB 저장

### ✔ 2. 공학 계산기 (Scientific Calculator)
- Python `math` 모듈 기반 고급 계산 지원  
- `sin()`, `cos()`, `tan()`, `log()`, `sqrt()`, `pi` 등 다양한 함수 사용 가능  
- 안전한 eval 방식(내장 함수 제한)

### ✔ 3. 진수 변환 계산기 (Base Converter)
다음 명령어 형식으로 계산 가능:

| 입력 예시 | 설명 |
|----------|------|
| `bin 10` | 10 → 2진수 |
| `oct 10` | 10 → 8진수 |
| `hex 255` | 10 → 16진수 |
| `2to10 1011` | 2진수 → 10진수 |
| `8to10 77` | 8진수 → 10진수 |
| `16to10 FF` | 16진수 → 10진수 |

모든 결과는 FastAPI → PostgreSQL에 저장됩니다.

---

## 📂 프로젝트 구조

```
flask-calculator-API-main/
│
├── app.py                 # Flask 웹 UI 서버
├── api_server.py          # FastAPI 백엔드 API 서버
├── requirements.txt       # Python 의존성 목록
├── README.md              # 프로젝트 설명 파일
│
├── templates/
│   └── index.html         # UI 화면(계산기)
│
└── __pycache__/           # Python 캐시 파일
```

---

## 🗄️ 데이터베이스 구조 (PostgreSQL)

다음 테이블 3개가 필요합니다:

```sql
CREATE TABLE IF NOT EXISTS history (
    id SERIAL PRIMARY KEY,
    expression TEXT,
    result TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sci_history (
    id SERIAL PRIMARY KEY,
    expression TEXT,
    result TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS base_history (
    id SERIAL PRIMARY KEY,
    expression TEXT,
    result TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🛠 기술 스택

| Layer | Tech |
|-------|------|
| Frontend | Flask (Jinja2 Template) |
| Backend API | FastAPI |
| Database | PostgreSQL |
| Language | Python 3.x |
| 웹통신 | REST API(JSON) |
| 서버 실행 | uvicorn, Flask dev server |

---

## 🚀 실행 방법

### 1) FastAPI 실행 (포트 8001)

```bash
uvicorn api_server:app --reload --port 8001
```

### 2) Flask 실행 (포트 5000)

```bash
python app.py
```

웹 브라우저 접속:

- **Flask UI** → http://127.0.0.1:5000  
- **FastAPI Docs** → http://127.0.0.1:8001/docs

---

## 📌 API 엔드포인트 목록 (FastAPI)

| Method | Endpoint | 기능 |
|--------|----------|------|
| POST | `/calc` | 일반 계산기 결과 저장 |
| POST | `/sci_calc` | 공학 계산기 결과 저장 |
| POST | `/base_calc` | 진수 계산 결과 저장 |
| GET | `/history` | 일반 계산기 이력 조회 |
| GET | `/sci_history` | 공학 계산기 이력 조회 |
| GET | `/base_history` | 진수 변환 이력 조회 |
| DELETE | `/history` | 일반 계산 이력 삭제 |
| DELETE | `/sci_history` | 공학 계산 이력 삭제 |
| DELETE | `/base_history` | 진수 변환 이력 삭제 |

---

## 🧪 테스트 예시

### 🔹 일반 계산기
```
(3+2)*5
```

### 🔹 공학 계산기
```
sin(3.14)
log(10)
sqrt(64)
```

### 🔹 진수 계산기
```
bin 10
hex 255
2to10 1011
16to10 FF
```

---

## 🧩 향후 추가 예정 기능

- Bootstrap 기반 UI 개선  
- 진수 자동 감지 기능 (0b / 0o / 0x 자동 판단)  
- Dockerfile 포함한 배포 패키지  
- GitHub Actions CI/CD  
- 사용자 로그인 기능(기록 개인별 저장)  

---

## 📜 라이선스

MIT License

---

## 🙌 기여

Pull Request 환영합니다!  
버그/개선 제안은 Issue로 남겨주세요.
