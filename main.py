from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ===== FastAPI instance =====
app = FastAPI()

# ===== Folder static =====
app.mount("/static", StaticFiles(directory="static"), name="static")

# ===== Folder HTML template =====
templates = Jinja2Templates(directory="templates")

# ===== Dummy user (buat latihan) =====
USER_DATA = {
    "lorem": "12345"
}


# ========================
# LOGIN PAGE
# ========================
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in USER_DATA and USER_DATA[username] == password:
        response = RedirectResponse(url="/landing", status_code=303)
        response.set_cookie(key="user", value=username)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Login gagal!"})


# ========================
# LANDING PAGE
# ========================
@app.get("/landing")
async def landing_page(request: Request):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("landing.html", {"request": request, "user": user})


# ========================
# DASHBOARD
# ========================
@app.get("/dashboard")
async def dashboard_page(request: Request):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


# ========================
# LOGOUT
# ========================
@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user")
    return response
