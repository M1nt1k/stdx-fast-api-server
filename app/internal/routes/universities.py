from fastapi import APIRouter
import os
from app.pkg.mongo_tools.tools import MongoTools

router = APIRouter(
    prefix=f'/api/v{os.getenv("VERSION")}/universities',
    tags=['Universities']
)

collection = 'universities'

@router.get('/')
async def get_universities():
    res = []
    universities = await MongoTools.find(collection=collection, filter={})
    for university in await universities.to_list(length=9999):
        res.append(university)
    return res
