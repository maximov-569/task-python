from contextlib import asynccontextmanager
from fastapi import FastAPI

import os
import sys

sys.path.append(os.path.join(os.getcwd(), ".."))

from src.service_state.router import router as service_state_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(service_state_router)
