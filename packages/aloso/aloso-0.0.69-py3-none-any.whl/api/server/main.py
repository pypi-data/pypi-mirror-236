import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import config
from api.server.auth import check_api_key
from api.server.router import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, dependencies=[Depends(check_api_key)])

if __name__ == '__main__':
    uvicorn.run("api.server.main:app", port=8006, reload=True, reload_includes=config.root_dir)
