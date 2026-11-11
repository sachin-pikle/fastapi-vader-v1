from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class ReviewRequest(BaseModel):
    text: str


app = FastAPI(title="FastAPI VADER Demo")
analyzer = SentimentIntensityAnalyzer()


@app.post("/api/reviews/analyze")
def analyze_review(request: ReviewRequest) -> dict[str, str | float]:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Review text must not be blank.")

    scores = analyzer.polarity_scores(request.text)
    compound = float(scores["compound"])

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "compound": compound,
        "positive": float(scores["pos"]),
        "neutral": float(scores["neu"]),
        "negative": float(scores["neg"]),
    }


static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
