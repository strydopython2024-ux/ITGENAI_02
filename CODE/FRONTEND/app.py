import os, requests
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-change-this-secret")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


def api_request(method, path, **kwargs):
    try:
        timeout = kwargs.pop("timeout", 10)
        r = requests.request(method, BACKEND_URL + path, timeout=timeout, **kwargs)
        try:
            data = r.json()
        except ValueError:
            return {
                "success": False,
                "message": "Backend returned an invalid response.",
            }, r.status_code
        if r.status_code >= 400:
            return data, r.status_code
        return data, r.status_code
    except requests.RequestException:
        return {
            "success": False,
            "message": "Backend is unavailable. Start FastAPI on port 8000.",
        }, 503


def login_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if "user" not in session:
            return redirect(url_for("auth"))
        return f(*a, **kw)

    return wrapper


def profile():
    return api_request("GET", "/api/analysis/profile")[0]


@app.route("/")
def index():
    return (
        redirect(url_for("dashboard"))
        if "user" in session
        else redirect(url_for("auth"))
    )


@app.route("/auth", methods=["GET", "POST"])
def auth():
    mode = request.args.get("mode", "login")
    if request.method == "POST":
        action = request.form.get("action", "login")
        if action == "register":
            if request.form.get("password") != request.form.get("confirm_password"):
                flash("Passwords do not match.", "error")
                return render_template("auth.html", mode="register")
            data, status = api_request(
                "POST",
                "/api/auth/register",
                json={
                    "name": request.form.get("name", ""),
                    "email": request.form.get("email", ""),
                    "password": request.form.get("password", ""),
                },
            )
            if data.get("success"):
                flash("Registration successful. Please sign in.", "success")
                return redirect(url_for("auth", mode="login"))
            flash(data.get("message", "Registration failed."), "error")
            return render_template("auth.html", mode="register")
        data, status = api_request(
            "POST",
            "/api/auth/login",
            json={
                "email": request.form.get("email", ""),
                "password": request.form.get("password", ""),
            },
        )
        if data.get("success"):
            session["user"] = data["user"]
            return redirect(url_for("dashboard"))
        flash(data.get("message", "Login failed."), "error")
    return render_template("auth.html", mode=mode)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard", profile=profile())


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        f = request.files.get("file")
        if not f or not f.filename:
            flash("Select a CSV file.", "error")
            return render_template("upload.html")
        data, status = api_request(
            "POST",
            "/api/data/upload",
            files={"file": (f.filename, f.stream, f.mimetype or "text/csv")},
            timeout=60,
        )
        if data.get("success"):
            flash(
                f"Uploaded {data.get('filename')} — {data.get('rows')} rows, {data.get('columns')} columns.",
                "success",
            )
            return redirect(url_for("dashboard"))
        flash(data.get("message", "Upload failed."), "error")
    return render_template("upload.html", title="Upload Data")


@app.route("/overview")
@login_required
def overview():
    p = profile()
    d = api_request("GET", "/api/data")[0]
    return render_template("overview.html", title="Data Overview", profile=p, data=d)


@app.route("/statistics")
@login_required
def statistics():
    p = profile()
    col = (
        request.args.get("column")
        or (p.get("column_types", {}).get("numeric") or [None])[0]
    )
    result = (
        api_request("GET", "/api/analysis/statistics", params={"column": col})[0]
        if col
        else {"success": False, "message": "No numeric column available."}
    )
    return render_template(
        "statistics.html", title="Statistical Analysis", profile=p, result=result
    )


@app.route("/categorical")
@login_required
def categorical():
    p = profile()
    col = (
        request.args.get("column")
        or (p.get("column_types", {}).get("categorical") or [None])[0]
    )
    result = (
        api_request("GET", "/api/analysis/categorical", params={"column": col})[0]
        if col
        else {"success": False, "message": "No categorical column available."}
    )
    return render_template(
        "categorical.html", title="Categorical Analysis", profile=p, result=result
    )


@app.route("/correlation")
@login_required
def correlation():
    return render_template(
        "correlation.html",
        title="Correlation Analysis",
        profile=profile(),
        result=api_request("GET", "/api/analysis/correlation")[0],
    )


@app.route("/forecasting", methods=["GET", "POST"])
@login_required
def forecasting():
    p = profile()
    dates = p.get("column_types", {}).get("date", [])
    nums = p.get("column_types", {}).get("numeric", [])
    result = None
    if request.method == "POST":
        result = api_request(
            "GET",
            "/api/analysis/forecast",
            params={
                "date_column": request.form.get("date_column"),
                "target": request.form.get("target"),
                "horizon": request.form.get("horizon", "7"),
            },
            timeout=30,
        )[0]
    return render_template(
        "forecasting.html",
        title="Forecasting",
        profile=p,
        dates=dates,
        nums=nums,
        result=result,
    )


@app.route("/segmentation", methods=["GET", "POST"])
@login_required
def segmentation():
    p = profile()
    nums = p.get("column_types", {}).get("numeric", [])
    result = None
    if request.method == "POST":
        result = api_request(
            "GET",
            "/api/analysis/segmentation",
            params={
                "columns": ",".join(request.form.getlist("columns")),
                "k": request.form.get("k", "3"),
            },
            timeout=30,
        )[0]
    return render_template(
        "segmentation.html", title="Segmentation", profile=p, nums=nums, result=result
    )


@app.route("/anomalies", methods=["GET", "POST"])
@login_required
def anomalies():
    p = profile()
    nums = p.get("column_types", {}).get("numeric", [])
    result = None
    if request.method == "POST":
        result = api_request(
            "GET",
            "/api/analysis/anomalies",
            params={"columns": ",".join(request.form.getlist("columns"))},
            timeout=30,
        )[0]
    return render_template(
        "anomalies.html", title="Anomaly Detection", profile=p, nums=nums, result=result
    )


@app.route("/ai", methods=["GET"])
@login_required
def ai_insights():
    return render_template("ai.html", title="AI Business Analyst", profile=profile())


@app.context_processor
def inject():
    return {"current_user": session.get("user"), "backend_url": BACKEND_URL}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
