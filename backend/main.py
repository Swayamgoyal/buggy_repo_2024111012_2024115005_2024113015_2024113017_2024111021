from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import items, analytics, quiz
from routes import users as users_router

app = FastAPI()

# Include routers for different features
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(users_router.router, prefix="/users", tags=["users"])

# Add CORS middleware if frontend and backend are on different origins
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
