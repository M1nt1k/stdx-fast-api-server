from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from bson import ObjectId
from datetime import datetime
from pprint import pprint
from app.pkg.mongo_tools.tools import MongoTools


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


'''User's model'''

class StatusModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: str
    icon: str

class UserModel(BaseModel):
    vk: str = Field(..., alias="_id")
    disabled: bool = False
    status: List[StatusModel] | None = None

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "vk": "123456789",
                "disabled": False,
                "status": []
            }
        }

class User(UserModel):
    hashed_password: str


'''Category's model'''

class CategoryModel(BaseModel):
    category: str = Field(..., alias="_id")

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'category': 'Метрология'
            }
        }


'''University's model'''

class UniversityModel(BaseModel):
    university: str = Field(..., alias="_id")

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'university': 'ТИУ'
            }
        }


'''File's model'''

class FileModel(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    path: str


'''Responce's model'''

class ResponceModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    text: str
    price: int
    deliveryDate: str

    owner: UserModel
    created: str = datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M')

    # @validator("deliveryDate", pre=True)
    # def parse_deliveryDate(cls, value):
    #     return datetime.strptime(
    #         value,
    #         '%d.%m.%Y %H:%M'
    #     )
    
    # @validator("created", pre=True)
    # def parse_created(cls, value):
    #     return datetime.strptime(
    #         value,
    #         '%d.%m.%Y %H:%M'
    #     )
    
    # @validator("owner", pre=True)
    # async def check_link(cls, value):
    #     user = await MongoTools.find_one('users', {'vk_id': value})
    #     if user:
    #         return user['_id']

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                'text': 'Готов выполнить задание!',
                'price': 1200,
                'deliveryDate': '12.12.2023 14:10',
                'owner': {
                    '_id': '123456789'
                },
                'created': '12.12.2000 14:10',
            }
        }
    
    


'''Task's model'''

class TaskModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    category: CategoryModel
    university: UniversityModel
    orderDate: str = datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M')
    deliveryDate: str
    files: List[FileModel] = []
    is_published: bool = False
    owner: UserModel
    responces: List[ResponceModel] = []

    # @validator("orderDate", pre=True)
    # def parse_date(cls, value):
    #     return datetime.strptime(
    #         value,
    #         '%d.%m.%Y %H:%M'
    #     )
    
    # @validator("deliveryDate", pre=True)
    # def parse_deliveryDate(cls, value):
    #     return datetime.strptime(
    #         value,
    #         '%d.%m.%Y %H:%M'
    #     )

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Сделать метрологию",
                "description": "ПАМАГИТЕ",
                "category":  {
                    "category": "Метрология"
                },
                "university": {
                    "university": "ТИУ"
                },
                "orderDate": "05.05.2023 14:00",
                "deliveryDate": "12.05.2023 14:00",
                "files": [],
                "is_published": True,
                "owner": {
                    "vk": "123456789"
                },
                "responces": [],
            }
        }


class UTaskModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    category: Optional[CategoryModel]
    university: Optional[UniversityModel]
    deliveryDate: Optional[datetime]
    files: Optional[List[FileModel]] = []
    is_published: Optional[bool] = False
    responces: Optional[List[ResponceModel]] = []
    
    @validator("deliveryDate", pre=True)
    def parse_deliveryDate(cls, value):
        return datetime.strptime(
            value,
            '%d.%m.%Y %H:%M'
        )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Сделать метрологию",
                "description": "ПАМАГИТЕ",
                "category":  {
                    "category": "Метрология"
                },
                "university": {
                    "university": "ТИУ"
                },
                "orderDate": "05.05.2023 14:00",
                "deliveryDate": "12.05.2023 14:00",
                "files": [],
                "is_published": True,
                "owner": {
                    "vk": "123456789"
                },
                "responces": [],
            }
        }


'''Token's model'''

class Token(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    acces_token: str
    token_type: str

class TokenData(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    vk_id: str