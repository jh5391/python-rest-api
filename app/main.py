from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import user, post, auth, reply
from .log import LoggingMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(post.router)
app.include_router(reply.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
