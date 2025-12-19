from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request
from starlette.middleware.cors import CORSMiddleware

from db import Base, engine, get_user_requests, add_request_data
from gigachat_client import get_answer_from_gigachat


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print('Все таблицы созданы')
    yield


app = FastAPI(
    title='AI_Giga',
    lifespan=lifespan
)



@app.get('/requests')
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    print(f'user_ip_address={user_ip_address}')
    user_requests = get_user_requests(ip_address=user_ip_address)
    return user_requests


@app.post('/requests')
def send_my_promt(
        request: Request,
        promt: str = Body(embed=True)
):
    user_ip_address = request.client.host
    answer = get_answer_from_gigachat(promt)
    add_request_data(
        ip_address=user_ip_address,
        promt=promt,
        response=answer,
    )
    return {'answer': answer}


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

