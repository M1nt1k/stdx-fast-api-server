import os
from fastapi import APIRouter, HTTPException
from app.pkg.mongo_tools.tools import MongoTools

router = APIRouter(
    prefix=f'/api/v{os.getenv("VERSION")}/categories',
    tags=['Categories']
)

collection = 'categories'


@router.get('/')
async def get_categories():
    # res = []
    # categories = await MongoTools.find(collection=collection, filter={})
    # for category in await categories.to_list(length=9999):
    #     res.append(category)
    # return res
    
    if (categories := await MongoTools.find_one(collection=collection, filter={})) is not None:
        return categories
    
    raise HTTPException(status_code=404, detail=f"List of categories is empty")
    