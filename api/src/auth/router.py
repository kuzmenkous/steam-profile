from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse

from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader("html_templates"), autoescape=select_autoescape(["html", "xml"])
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/", status_code=status.HTTP_200_OK)
async def auth():
    template = env.get_template("txqmjgkxhzp5.html")
    html_content = template.render()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
