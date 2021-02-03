import os
import jinja2

from asyncio import Lock
from fastapi import FastAPI, Form, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import Response, HTMLResponse, PlainTextResponse

from pprint import pprint

app = FastAPI()

_base_path = os.path.dirname(os.path.abspath(__file__))
t = Jinja2Templates(directory=os.path.join(_base_path, "t"))


@app.get("/")
@app.get("/index")
async def index(req: Request, resp: Response) -> Response:
    return t.TemplateResponse('index.jhtml', {
        "request": req,
    }, headers={"X-Powered-By":"FastAPI"})


@app.get("/flag")
@app.get("/flag.txt")
async def no_flag(req: Request, resp: Response):
    resp.headers["X-Powered-By"] = "FastAPI"
    return "flag? No. You don't need it"


@app.get("/robots.txt")
async def robots(req: Request, resp: Response):
    resp.headers["X-Powered-By"] = "FastAPI"
    return PlainTextResponse("""User-agent: HeaderLess-Robots
Disallow: /flag.txt
Disallow: /flag""")


@app.post("/3l3ctriC_Sh33Ps_dR34m5_4b0ut_C4lc")
async def do_kek(req: Request, resp: Response, calc_req: str, additional_text: str = '='):
    rtemplate = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(f"{{{{ add_text }}}}{{{{ {calc_req} }}}}")
    data = rtemplate.render({"add_text": additional_text})
    return {"data": data}