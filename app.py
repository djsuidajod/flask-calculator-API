from flask import Flask, render_template, request, redirect, url_for, flash
import re, math, requests

app = Flask(__name__)
app.secret_key = "change-this"

API_URL = "http://127.0.0.1:8001"


# --------------------------------------------------
# 수식 파서 (일반 계산기)
# --------------------------------------------------
def skip_spaces(expr):
    return expr.lstrip()

def parse_number(expr):
    expr = skip_spaces(expr)
    m = re.match(r'\d+(\.\d+)?', expr)
    if not m:
        raise ValueError("숫자가 필요합니다.")
    num = float(m.group())
    return num, expr[len(m.group()):]

def parse_factor(expr):
    expr = skip_spaces(expr)
    if expr.startswith('('):
        val, rest = parse_expression(expr[1:])
        rest = skip_spaces(rest)
        if not rest.startswith(')'):
            raise ValueError("')'가 필요합니다.")
        return val, rest[1:]
    return parse_number(expr)

def parse_term(expr):
    val, rest = parse_factor(expr)
    while True:
        rest = skip_spaces(rest)
        if rest.startswith('*'):
            nv, rest = parse_factor(rest[1:]); val *= nv
        elif rest.startswith('/'):
            nv, rest = parse_factor(rest[1:]); val /= nv
        else:
            break
    return val, rest

def parse_expression(expr):
    val, rest = parse_term(expr)
    while True:
        rest = skip_spaces(rest)
        if rest.startswith('+'):
            nv, rest = parse_term(rest[1:]); val += nv
        elif rest.startswith('-'):
            nv, rest = parse_term(rest[1:]); val -= nv
        else:
            break
    return val, rest

def calculate_expression(expr):
    val, rem = parse_expression(expr)
    if skip_spaces(rem):
        raise ValueError("잘못된 수식입니다.")
    return val


# --------------------------------------------------
# 공학 계산기
# --------------------------------------------------
def calculate_scientific(expr):
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    code = compile(expr, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed:
            raise NameError(f"허용되지 않은 함수: {name}")
    return eval(code, {"__builtins__": {}}, allowed)


# --------------------------------------------------
# 진수 계산기
# --------------------------------------------------
def calculate_base(expr):
    parts = expr.split()
    if len(parts) != 2:
        raise ValueError("형식: [명령] [값]  예) bin 10 또는 2to10 1011")

    cmd, value = parts[0], parts[1]

    if cmd == "bin":      # 10 → 2
        return bin(int(value))[2:]

    if cmd == "oct":      # 10 → 8
        return oct(int(value))[2:]

    if cmd == "hex":      # 10 → 16
        return hex(int(value))[2:].upper()

    if cmd == "2to10":
        return str(int(value, 2))

    if cmd == "8to10":
        return str(int(value, 8))

    if cmd == "16to10":
        return str(int(value, 16))

    raise ValueError("지원하지 않는 진수 명령입니다.")


# --------------------------------------------------
# 메인 페이지
# --------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    try:
        rows_basic = requests.get(f"{API_URL}/history").json()
    except:
        rows_basic = []

    try:
        rows_sci = requests.get(f"{API_URL}/sci_history").json()
    except:
        rows_sci = []

    try:
        rows_base = requests.get(f"{API_URL}/base_history").json()
    except:
        rows_base = []

    return render_template(
        "index.html",
        rows_basic=rows_basic,
        rows_sci=rows_sci,
        rows_base=rows_base
    )


# --------------------------------------------------
# 계산 처리
# --------------------------------------------------
@app.route("/calc", methods=["POST"])
def calc():
    expr = (request.form.get("expression") or "").strip()
    mode = request.form.get("mode", "basic")

    if not expr:
        flash("수식을 입력하세요.")
        return redirect(url_for("index"))

    try:
        if mode == "basic":
            result = calculate_expression(expr)
            requests.post(f"{API_URL}/calc",
                          json={"expression": expr, "result": str(result)})

        elif mode == "sci":
            result = calculate_scientific(expr)
            requests.post(f"{API_URL}/sci_calc",
                          json={"expression": expr, "result": str(result)})

        else:
            raise ValueError("잘못된 모드")

        flash(f"결과: {result}")
    except Exception as e:
        flash(f"오류: {e}")

    return redirect(url_for("index"))


@app.route("/base_calc", methods=["POST"])
def base_calc():
    expr = (request.form.get("expression") or "").strip()

    try:
        result = calculate_base(expr)
        requests.post(f"{API_URL}/base_calc",
                      json={"expression": expr, "result": str(result)})
        flash(f"결과: {result}")
    except Exception as e:
        flash(f"오류: {e}")

    return redirect(url_for("index"))


# --------------------------------------------------
# 이력 삭제
# --------------------------------------------------
@app.route("/history/clear", methods=["POST"])
def history_clear():
    requests.delete(f"{API_URL}/history")
    flash("일반 계산기 이력 삭제 완료")
    return redirect(url_for("index"))

@app.route("/sci_history/clear", methods=["POST"])
def sci_history_clear():
    requests.delete(f"{API_URL}/sci_history")
    flash("공학 계산기 이력 삭제 완료")
    return redirect(url_for("index"))

@app.route("/base_history/clear", methods=["POST"])
def base_history_clear():
    requests.delete(f"{API_URL}/base_history")
    flash("진수 계산기 이력 삭제 완료")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
