# 🧮 Flask + FastAPI Calculator

Flask 웹 UI와 FastAPI 백엔드, PostgreSQL 데이터베이스를 결합한  
**일반/공학 계산기** 프로젝트입니다.

---

## ✨ 주요 기능
- **일반 계산기** : 사칙연산 및 괄호 계산
- **공학 계산기** : `sin`, `log`, `sqrt` 등 `math` 모듈 기반 수식
- **FastAPI 백엔드** : REST API로 계산 결과 저장 및 이력 조회/초기화
- **PostgreSQL** : 일반·공학 계산 이력 별도 테이블 관리

---

## 🛠 기술 스택
| 영역         | 기술 |
|--------------|-----|
| Frontend     | Flask (Jinja2) |
| Backend API  | FastAPI |
| Database     | PostgreSQL |
| Language     | Python 3.13 |

---

## 🚀 실행 방법

### 1. FastAPI 백엔드
```bash
uvicorn api_server:app --reload --port 8001
```
- Swagger UI: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

### 2. Flask 프론트엔드
```bash
python app.py
```
- 웹 UI: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 💾 데이터베이스 준비
PostgreSQL에서 아래 테이블을 만들어 주세요.
```sql
CREATE TABLE IF NOT EXISTS history (
    id SERIAL PRIMARY KEY,
    expression TEXT,
    result DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sci_history (
    id SERIAL PRIMARY KEY,
    expression TEXT,
    result DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📂 프로젝트 구조
```
flask-calculator-main/
├─ app.py              # Flask 서버
├─ api_server.py       # FastAPI 백엔드
├─ requirements.txt    # 의존성
├─ templates/
│   └─ index.html      # 메인 UI
└─ README.md
```

---

## 🔧 주요 API (FastAPI)
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/calc`       | 일반 계산 결과 저장 |
| POST | `/sci_calc`   | 공학 계산 결과 저장 |
| GET  | `/history`    | 일반 계산 이력 조회 |
| GET  | `/sci_history`| 공학 계산 이력 조회 |
| DELETE | `/history`    | 일반 이력 초기화 |
| DELETE | `/sci_history`| 공학 이력 초기화 |

---

## 🖼️ 스크린샷 (예시)
> 필요하면 `docs/screenshot.png` 를 추가 후 링크하세요.

---

## 📜 라이선스
MIT License
