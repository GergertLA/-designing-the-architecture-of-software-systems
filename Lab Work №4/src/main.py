from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, List

app = FastAPI(title="News Sentiment API")

news_sources: Dict[UUID, dict] = {}
news_items: Dict[UUID, dict] = {}

class NewsSourceCreate(BaseModel):
    name: str
    url: str
    type: str


class NewsSource(NewsSourceCreate):
    id: UUID
    created_at: datetime


class NewsCreate(BaseModel):
    title: str
    content: str
    sentiment: float
    source_id: UUID
    published_at: datetime


class News(NewsCreate):
    id: UUID


@app.post("/api/v1/sources", response_model=NewsSource, status_code=201)
def create_source(request: NewsSourceCreate):
    source_id = uuid4()
    source = {
        "id": source_id,
        "name": request.name,
        "url": request.url,
        "type": request.type,
        "created_at": datetime.utcnow()
    }
    news_sources[source_id] = source
    return source


@app.get("/api/v1/sources", response_model=List[NewsSource])
def get_sources():
    return list(news_sources.values())


@app.get("/api/v1/sources/{source_id}", response_model=NewsSource)
def get_source(source_id: UUID):
    if source_id not in news_sources:
        raise HTTPException(status_code=404, detail="Source not found")
    return news_sources[source_id]


@app.put("/api/v1/sources/{source_id}", response_model=NewsSource)
def update_source(source_id: UUID, request: NewsSourceCreate):
    if source_id not in news_sources:
        raise HTTPException(status_code=404, detail="Source not found")

    source = news_sources[source_id]
    source.update(
        name=request.name,
        url=request.url,
        type=request.type
    )
    return source


@app.delete("/api/v1/sources/{source_id}")
def delete_source(source_id: UUID):
    if source_id not in news_sources:
        raise HTTPException(status_code=404, detail="Source not found")

    del news_sources[source_id]
    return {"status": "deleted"}


@app.post("/api/v1/news", status_code=201)
def create_news(request: NewsCreate):
    if request.source_id not in news_sources:
        raise HTTPException(status_code=404, detail="Source not found")

    news_id = uuid4()
    item = {
        "id": news_id,
        "title": request.title,
        "content": request.content,
        "sentiment": request.sentiment,
        "source_id": request.source_id,
        "published_at": request.published_at
    }
    news_items[news_id] = item
    return {"id": news_id, "status": "created"}


@app.get("/api/v1/news", response_model=List[News])
def get_news():
    return list(news_items.values())


@app.get("/api/v1/news/{news_id}", response_model=News)
def get_news_by_id(news_id: UUID):
    if news_id not in news_items:
        raise HTTPException(status_code=404, detail="News not found")
    return news_items[news_id]


@app.put("/api/v1/news/{news_id}", response_model=News)
def update_news(news_id: UUID, request: NewsCreate):
    if news_id not in news_items:
        raise HTTPException(status_code=404, detail="News not found")

    news_items[news_id].update(
        title=request.title,
        content=request.content,
        sentiment=request.sentiment,
        source_id=request.source_id,
        published_at=request.published_at
    )
    return news_items[news_id]


@app.delete("/api/v1/news/{news_id}")
def delete_news(news_id: UUID):
    if news_id not in news_items:
        raise HTTPException(status_code=404, detail="News not found")

    del news_items[news_id]
    return {"status": "deleted"}
