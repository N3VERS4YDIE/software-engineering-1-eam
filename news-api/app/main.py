from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import get_db
from app.entities.news_article_entity import NewsArticleEntity
from app.entities.newspaper_entity import NewspaperEntity
from app.routes.routes import router

db = get_db()

# Create the FastAPI app
app = FastAPI(
    title="News API",
    description="API for managing newspapers and news articles",
    version="1.0.0",
)

# CORS setup (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the API router with all routes from newspapers and news articles
app.include_router(router)


# Optional: You can add startup and shutdown events here if needed
@app.on_event("startup")
async def startup_event():
    print("Creating tables...")
    with db:
        db.create_tables([NewspaperEntity, NewsArticleEntity])


@app.on_event("shutdown")
async def shutdown_event():
    print("Closing database connection...")
    if not db.is_closed():
        db.close()


# Run the app (only needed if you are running this file directly)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
