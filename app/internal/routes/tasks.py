from fastapi import APIRouter, Body, HTTPException, status, UploadFile
from datetime import datetime
from app.internal.schemas import models
from app.internal.schemas.models import PyObjectId
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger

import os

from app.pkg.mongo_tools.tools import MongoTools

router = APIRouter(
    prefix=f'/api/v{os.getenv("VERSION")}/tasks',
    tags=['Tasks']
)

collection = 'tasks'


'''Tasks'''

@router.get('/') #, response_model=models.TaskModel
async def get_tasks(limit:int = 100, often: int = 100, page: int = 1):
    res = []
    tasks = await MongoTools.find(collection=collection, filter={}, limit=limit, often=often, page=page)
    for task in await tasks.to_list(length=limit):
        res.append(task)
    return res

@router.post('/', response_model=models.TaskModel)
async def add_tasks(task: models.TaskModel):
    document = jsonable_encoder(task)
    new_task = await MongoTools.insert_one(collenction=collection, document=document)
    created_task = await MongoTools.find_one(collection=collection, filter={"_id": new_task.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)
    

@router.get('/{task_id}') #, response_model=models.TaskModel
async def get_task(task_id: str):
    if (task :=  await MongoTools.find_one(collection=collection, filter={"_id": task_id})) is not None:
        return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@router.put('/{task_id}')
async def put_task(task_id: str, task: dict = Body(...)):
    document = jsonable_encoder(task)

    updated_task = await MongoTools.update_one(collection=collection, id=task_id, document=document)
    created_task = await MongoTools.find_one(collection=collection, filter={"_id": task_id})

    return JSONResponse(status_code=status.HTTP_200_OK, content=created_task)


@router.delete('/{task_id}')
async def delete_task(task_id: str):
    result = await MongoTools.delete_one(collection=collection, id=task_id) # 6459131ffb7ae7ea3dfbcc40

    return JSONResponse(status_code=status.HTTP_200_OK, content={'result': 'Удаление произведено успешно'})

'''Responces'''

@router.get('/{task_id}/responces', responce_model=models.ResponceModel)
async def get_responces(task_id: str, responce: models.ResponceModel):
    document = jsonable_encoder(responce)
    new_resp = await MongoTools.update_one(collenction=collection, id=task_id, document=document)
    created_resp = await MongoTools.find_one(collection=collection, document={'_id': task_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_resp['responces'])

@router.get('/{task_id}/responces/{resp_id}')
async def get_responce(task_id: str, resp_id: str):
    ...

@router.put('/{task_id}/responces/{resp_id}')
async def put_responce(task_id: str, resp_id: str):
    ...

@router.delete('/{task_id}/responces/{resp_id}')
async def delete_responce(task_id: str, resp_id: str):
    ...

'''Files'''

@router.get('/{task_id}/files')
async def get_files(task_id: str):
    if (task :=  await MongoTools.find_one(collection=collection, filter={"_id": task_id})) is not None:
        return task['files']

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@router.post('/{task_id}/files')
async def save_file():
    ...

@router.get('/{task_id}/files/{file_id}')
async def get_file(task_id: str, file_id: str):
    ...

@router.put('/{task_id}/files/{file_id}')
async def put_file(task_id: str, file_id: str):
    ...

@router.delete('/{task_id}/files/{file_id}')
async def delete_file(task_id: str, file_id: str):
    ...