from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.auth_service import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/github")
async def github_login():
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.GITHUB_REDIRECT_URI}"
        f"&scope=user:email"
        f"&prompt=login"
    )
    return RedirectResponse(url=github_auth_url)

@router.get("/github/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            token_response = await client.post(token_url, data=data, headers=headers)
            token_response.raise_for_status()
            token_data = token_response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"GitHub token request failed: {e}")
            
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to get access token from GitHub")
            
        user_url = "https://api.github.com/user"
        user_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        try:
            user_response = await client.get(user_url, headers=user_headers)
            user_response.raise_for_status()
            github_user = user_response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"GitHub user request failed: {e}")
            
    github_id_val = github_user.get("id")
    if not github_id_val:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid GitHub user data")
        
    github_id = int(github_id_val)
    username = github_user.get("login")
    email = github_user.get("email")
    avatar_url = github_user.get("avatar_url")
    
    stmt = select(User).where(User.github_id == github_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            github_id=github_id,
            username=username,
            email=email,
            avatar_url=avatar_url,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    jwt_token = create_access_token({"sub": str(user.id)})
    
    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000/")
    redirect_url = f"{frontend_url}?token={jwt_token}"
    return RedirectResponse(url=redirect_url)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
