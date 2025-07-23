from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from query_engine import process_question

app = FastAPI()

# Serve chart.html if generated
app.mount("/static", StaticFiles(directory="."), name="static")

templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "answer": ""})

@app.post("/", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    answer = process_question(question)
    show_chart = "chart.html" in answer
    return templates.TemplateResponse("index.html", {"request": request, "answer": answer, "show_chart": show_chart})
