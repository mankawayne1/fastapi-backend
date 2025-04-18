from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --- MODELS ---
class SummarizeRequest(BaseModel):
    content: str

class SummarizeResponse(BaseModel):
    summary: str

class FetchTrendsRequest(BaseModel):
    sources: List[str]
    keywords: List[str]

class FetchTrendsResponse(BaseModel):
    trends: List[str]
    questions: List[str]
    gaps: List[str]

class GeneratePostRequest(BaseModel):
    platform: str
    topic: str

class GeneratePostResponse(BaseModel):
    post: str

class SchedulePostRequest(BaseModel):
    platform: str
    post: str
    datetime: str

class SchedulePostResponse(BaseModel):
    status: str
    id: Optional[str] = None

class ApproveReplyRequest(BaseModel):
    platform: str
    comment_id: str
    reply_text: str
    approve: bool

class ApproveReplyResponse(BaseModel):
    status: str

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Render!"}

@app.post("/research/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    # Dummy summary logic
    return SummarizeResponse(summary=f"Summary of: {request.content}")

import os
import praw

@app.post("/research/fetch-trends", response_model=FetchTrendsResponse)
def fetch_trends(request: FetchTrendsRequest):
    trends = []
    if "reddit" in [s.lower() for s in request.sources]:
        reddit = praw.Reddit(
            client_id=os.getenv("wrXt143D1tNsbd8yYr9RHA"),
            client_secret=os.getenv("xZuLAExIYss4VaU6R1fFR33-g4qQEQ"),
            user_agent=os.getenv("eavy-Bonus1597")
        )
        for keyword in request.keywords:
            for submission in reddit.subreddit("all").search(keyword, limit=5, sort="top"):
                trends.append(submission.title)
    # questions and gaps extraction can be added here
    return FetchTrendsResponse(
        trends=trends,
        questions=[],
        gaps=[]
    )

@app.post("/scheduler/generate-post", response_model=GeneratePostResponse)
def generate_post(request: GeneratePostRequest):
    # Dummy post logic
    return GeneratePostResponse(post=f"Generated post for {request.platform} on {request.topic}")

@app.post("/scheduler/schedule-post", response_model=SchedulePostResponse)
def schedule_post(request: SchedulePostRequest):
    # Dummy schedule logic
    return SchedulePostResponse(status="scheduled", id="12345")

@app.post("/scheduler/approve-reply", response_model=ApproveReplyResponse)
def approve_reply(request: ApproveReplyRequest):
    # Dummy approval logic
    return ApproveReplyResponse(status="approved" if request.approve else "rejected")

