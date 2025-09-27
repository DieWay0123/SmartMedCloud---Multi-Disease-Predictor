import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import file, mapping_key, mapping_value, predict
from settings import settings


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

app.include_router(file.router)
app.include_router(mapping_key.router)
app.include_router(mapping_value.router)
app.include_router(predict.router)

@app.get("/")
def hello():
    return {"message": "Hello, world!"}

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, host=settings.app_host, port=settings.app_port)
