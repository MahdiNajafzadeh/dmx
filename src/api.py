"""
name: api.py
description: FastAPI REST API endpoints for download management
"""

import uvicorn
from fastapi import FastAPI
from database import File
from loop import Code, loop
from config import config

app = FastAPI()


@app.get("/download")
async def get_all_download():
    return loop.request(Code.REQ_FILE_GET_ALL)


@app.get("/download/{id}")
async def get_download(id: int):
    return loop.request(Code.REQ_FILE_GET, id)


@app.post("/download")
async def create_download(download: File):
    return loop.request(Code.REQ_FILE_CREATE, download)


@app.patch("/download/{id}")
async def update_download(id: int, download: File):
    return loop.request(Code.REQ_FILE_UPDATE, id, download)


@app.delete("/download/{id}")
async def delete_download(id: int):
    return loop.request(Code.REQ_FILE_DELETE, id)


@app.post("/download/{id}/start")
async def start_download(id: int):
    return loop.request(Code.REQ_FILE_START, id)


@app.post("/download/{id}/stop")
async def stop_download(id: int):
    return loop.request(Code.REQ_FILE_STOP, id)


def init():
    uvicorn.run(app=app, host=str(config["HOST"]), port=int(config["PORT"]))
