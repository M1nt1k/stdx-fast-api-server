FROM python:3.11.1

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install fastapi uvicorn redis aiohttp fastapi_utils python-multipart motor pydantic typing passlib[bcrypt] python-jose[cryptography]

COPY . /usr/src/app/