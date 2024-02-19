from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from settings import get_env_file_variables, update_env_file

from worker import process_archiver_task

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
templates = Jinja2Templates(directory="templates")


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse("templates/index.html")


@app.post("/lists_update", status_code=202)
async def index(
    sheets_url: str,
    proposal_date: str,
    deal: str,
    client: str,
    deal_id: int,
) -> dict:
    process_archiver_task.delay(
        table_key=sheets_url,
        proposal_date=proposal_date,
        deal=deal,
        client=client,
        deal_id=deal_id,
    )
    return {"status": "accepted"}


@app.get("/api/health", include_in_schema=False)
async def get_health():
    return {"status": "ok"}


@app.get("/settings", include_in_schema=False)
async def get_settings(request: Request):
    return templates.TemplateResponse(
        "settings.html", {"request": request, "settings": get_env_file_variables()}
    )


@app.post("/settings", include_in_schema=False)
async def save_settings(request: Request):
    form = await request.form()
    update_env_file(form)  # type: ignore
    return templates.TemplateResponse(
        "settings.html",
        {"request": request, "settings": get_env_file_variables(), "saved": True},
    )
