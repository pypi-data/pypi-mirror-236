import os

import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware

from laminhub_rest.routers import (
    account,
    ci,
    cloud_run,
    collaborator,
    deployment,
    dev,
    instance,
    organization,
    vault,
)

ROOT_PATH = "/" + os.getenv("ROOT_PATH", "")
PORT = int(os.getenv("PORT", 8000))


app = FastAPI(root_path=ROOT_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ci.router)
app.include_router(account.router)
app.include_router(instance.router)
app.include_router(collaborator.router)
app.include_router(dev.router)
app.include_router(organization.router)
app.include_router(cloud_run.router)
app.include_router(vault.router)
app.include_router(deployment.router)

client = TestClient(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, root_path=ROOT_PATH)
