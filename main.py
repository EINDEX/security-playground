import typing
from typing import Optional
import json
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from starlette.background import BackgroundTask
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class CustomResponse(Response):
    media_type = None

    def __init__(self, content: typing.Any = None, status_code: int = 200, headers: dict = None, media_type: str = None,
                 background: BackgroundTask = None) -> None:
        self.status_code = status_code
        if media_type is not None:
            self.media_type = media_type
        self.background = background
        self.body = self.render(content)
        self.raw_headers = []


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def header_form(params: dict = None) -> dict:
    if not params:
        params = {}
    with open('security_headers_config.json', 'r') as f:
        data = json.load(f)
        for key in data.keys():
            data[key]['default'] = params.get(key) or ''
        return data


def get_label_and_options_text_by_header_key_and_value(header_key: str, value: str) -> (str, str):
    return header_form({})[header_key]['label'], header_form({})[header_key]['options'][value]


@app.get("/security-headers/script-not-script.jpg", response_class=CustomResponse)
async def script_not_script():
    return """alert(1);"""


@app.get("/security-headers/referrer")
async def referrer(
        request: Request
):
    return templates.TemplateResponse("referrer_checking.html", {
        "request": request,
        "referrer": request.headers.get('Referer', ''),
    })


@app.get("/security-headers", response_class=HTMLResponse)
async def security_header(
        request: Request,
):
    headers = {}

    for header_key, option_key in request.query_params.items():
        if not option_key or header_key not in header_form():
            continue

        header, value = get_label_and_options_text_by_header_key_and_value(header_key, option_key)
        headers[header] = value
    return templates.TemplateResponse("security_headers.html", {
        "request": request,
        "headers": headers,
        "header_from": header_form(dict(request.query_params)),
    }, headers=headers)
