import os
from motor.motor_asyncio import AsyncIOMotorClient

class MongoTools:
    _client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    _db = _client['STDX']

    @classmethod
    def get_client(cls):
        return cls._client

    @classmethod
    async def find(cls, collection: str, filter: dict, limit: int = 0, often: int = 0, page: int = 1):
        documents = cls._db[collection].find(filter)
        if limit != 0:
            documents.limit(limit)
        if often != 0:
            documents.skip(often*(page-1)).limit(often)
        return documents
    
    @classmethod
    async def find_one(cls, collection: str, filter: dict):
        document = await cls._db[collection].find_one(filter)
        return document
    
    @classmethod
    async def insert_one(cls, collenction: str, document: dict):
        new_user = await cls._db[collenction].insert_one(document)
        return new_user
    
    @classmethod
    async def update_one(cls, collection: str, id: str, document: dict):
        update = await cls._db[collection].update_one({'_id': id},
                                        {'$set': document})
        return update
    
    @classmethod
    async def delete_one(cls, collection: str, id: str):
        result = await cls._db[collection].delete_one({'_id': id})
        return result

    
# _client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
# _db = _client['STDX']