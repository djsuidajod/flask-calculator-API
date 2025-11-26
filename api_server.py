from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2, os

app = FastAPI()

# ---------- PostgreSQL 연결 설정 ----------
DB_CONFIG = {
    "dbname": os.getenv("PG_DB", "mydb"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PW", "비밀번호"),   # 환경변수 사용 권장
    "host": os.getenv("PG_HOST", "localhost"),
    "port": int(os.getenv("PG_PORT", "5432")),
}

# ---------- 요청 데이터 모델 ----------
class CalcData(BaseModel):
    expression: str
    result: str  # 진수 문자열 지원 위해 문자열로 저장


# ---------- 일반 계산기 ----------
@app.post("/calc")
def insert_calc(data: CalcData):
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO history (expression, result) VALUES (%s, %s);",
            (data.expression, data.result)
        )
        conn.commit()
    return {"status": "ok"}


# ---------- 공학 계산기 ----------
@app.post("/sci_calc")
def insert_sci_calc(data: CalcData):
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO sci_history (expression, result) VALUES (%s, %s);",
            (data.expression, data.result)
        )
        conn.commit()
    return {"status": "ok"}


# ---------- 진수 계산기 ----------
@app.post("/base_calc")
def insert_base_calc(data: CalcData):
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO base_history (expression, result) VALUES (%s, %s);",
            (data.expression, data.result)
        )
        conn.commit()
    return {"status": "ok"}


# ---------- 조회 ----------
@app.get("/history")
def get_history():
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("SELECT id, expression, result, created_at FROM history ORDER BY id DESC;")
        rows = cur.fetchall()
    return [
        {"id": r[0], "expression": r[1], "result": r[2], "created_at": r[3].isoformat()}
        for r in rows
    ]


@app.get("/sci_history")
def get_sci_history():
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("SELECT id, expression, result, created_at FROM sci_history ORDER BY id DESC;")
        rows = cur.fetchall()
    return [
        {"id": r[0], "expression": r[1], "result": r[2], "created_at": r[3].isoformat()}
        for r in rows
    ]


@app.get("/base_history")
def get_base_history():
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("SELECT id, expression, result, created_at FROM base_history ORDER BY id DESC;")
        rows = cur.fetchall()
    return [
        {"id": r[0], "expression": r[1], "result": r[2], "created_at": r[3].isoformat()}
        for r in rows
    ]


# ---------- 초기화 ----------
@app.delete("/history")
def clear_history():
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE history RESTART IDENTITY;")
        conn.commit()
    return {"status": "cleared"}


@app.delete("/sci_history")
def clear_sci_history():
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE sci_history RESTART IDENTITY;")
        conn.commit()
    return {"status": "cleared"}


@app.delete("/base_history")
def clear_base_history():
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE base_history RESTART IDENTITY;")
        conn.commit()
    return {"status": "cleared"}
