from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.server import Server
from app.pkg.mongo_tools.tools import MongoTools


def app(_=None) -> FastAPI:
    
    app = FastAPI(
        debug=True,
        title='STDX',
        version='0.21.0'
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return Server(app).get_app()