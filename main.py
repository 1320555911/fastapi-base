import uvicorn
from utils.fastapi.applications import BaseFastAPI as FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from api import api_router
from settings import (
    CORS_ORIGINS_APP, DEBUG, RELOAD_DIRS
)

# 主app
docs_url = '/docs' if DEBUG else None
redoc_url = '/redoc' if DEBUG else None
app = FastAPI(title='fastapi-base', debug=DEBUG,
              version='2.0.0', description="fastapi基础框架",
              docs_url=docs_url, redoc_url=redoc_url)

app.include_router(api_router)

app.add_middleware(GZipMiddleware)

# 跨域
if CORS_ORIGINS_APP:
    app.add_middleware(CORSMiddleware,
                       allow_origins=CORS_ORIGINS_APP,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"])

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True,
                reload_dirs=RELOAD_DIRS)
