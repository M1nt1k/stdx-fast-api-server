import os
from fastapi import APIRouter
# from app.internal.database.db import db

router = APIRouter(
    prefix=f'/api/v{os.getenv("VERSION")}',
    tags=['About']
)


@router.get('/status')
def check_server_status():
    return 200, 'Server work'