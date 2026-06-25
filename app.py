from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    response = requests.get("https://dummyjson.com/products?limit=12")
    products = response.json()["products"]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "products": products
        }
    )


@app.get("/product/{id}", response_class=HTMLResponse)
async def product(request: Request, id: int):
    response = requests.get(f"https://dummyjson.com/products/{id}")
    product = response.json()

    return templates.TemplateResponse(
        request=request,
        name="product.html",
        context={
            "product": product
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)