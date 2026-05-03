from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.review import Review
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
async def get_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Review).where(Review.user_id == current_user.id).order_by(Review.created_at.desc())
    result = await db.execute(stmt)
    reviews = result.scalars().all()
    
    if not reviews:
        return {
            "total_reviews": 0,
            "avg_score": 0.0,
            "best_score": 0,
            "languages": {},
            "recent_scores": []
        }
        
    total_reviews = len(reviews)
    
    valid_scores = [r.score for r in reviews if r.score is not None]
    avg_score = round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else 0.0
    best_score = max(valid_scores) if valid_scores else 0
    
    languages: Dict[str, int] = {}
    for r in reviews:
        if r.language:
            languages[r.language] = languages.get(r.language, 0) + 1
            
    recent = reviews[:10]
    recent_scores = [
        {
            "date": r.created_at.strftime("%Y-%m-%d"),
            "score": r.score
        }
        for r in recent if r.score is not None
    ]
    
    return {
        "total_reviews": total_reviews,
        "avg_score": avg_score,
        "best_score": best_score,
        "languages": languages,
        "recent_scores": recent_scores
    }

@router.get("/trend")
async def get_trend(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Review).where(Review.user_id == current_user.id).order_by(Review.created_at.desc()).limit(20)
    result = await db.execute(stmt)
    reviews = result.scalars().all()
    
    reviews.reverse()
    
    trend = [
        {
            "review_id": r.id,
            "score": r.score,
            "language": r.language,
            "created_at": r.created_at.isoformat()
        }
        for r in reviews
    ]
    return trend
