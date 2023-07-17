from dataclasses import dataclass
from fastapi import FastAPI

__all__ = ['Controller']

@dataclass(frozen=True)
class Controller:
    def validate_data(self):
        ...

    
