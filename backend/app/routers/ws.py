from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import anthropic

from app.database import get_db
from app.models.review import Review
from app.services.claude_service import stream_code_review, extract_score, extract_issues, detect_language
from app.services.auth_service import get_user_from_token

router = APIRouter()

@router.websocket("/ws/review")
async def websocket_review(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    
    try:
        data = await websocket.receive_json()
        code = data["code"]
        hint = data.get("language", "")
        token = data.get("token")
        
        language = detect_language(code, hint)
        
        try:
            if not token:
                user = None
            else:
                user = await get_user_from_token(token, db)
        except Exception:
            user = None
            
        if user is None:
            await websocket.send_json({"type": "error", "message": "Unauthorized"})
            await websocket.close()
            return
            
        await websocket.send_json({"type": "started", "language": language})
        
        full_review = ""
        try:
            for chunk in stream_code_review(code, language):
                full_review += chunk
                await websocket.send_json({"type": "chunk", "content": chunk})
        except Exception as e:
            await websocket.send_json({"type": "error", "message": "AI service error"})
            await websocket.close()
            return
            
        score = extract_score(full_review)
        issues = extract_issues(full_review)
        
        review = Review(
            user_id=user.id,
            code=code,
            language=language,
            review_text=full_review,
            issues=issues,
            score=score
        )
        db.add(review)
        await db.commit()
        await db.refresh(review)
        
        await websocket.send_json({
            "type": "done",
            "review_id": review.id,
            "score": score,
            "language": language,
            "issue_count": len(issues)
        })
        
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
            await websocket.close()
        except RuntimeError:
            pass
