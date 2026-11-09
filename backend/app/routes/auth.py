from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.core.security import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

def _token_for_credentials(email: str, password: str, db: Session) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Ce compte est désactivé.")
    return {
        "access_token": create_access_token(user.id, user.role),
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role,
    }

@router.post(
    "/login",
    response_model=TokenResponse,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/LoginRequest"}
                },
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string", "title": "Email"},
                            "password": {"type": "string", "format": "password"},
                        },
                        "required": ["username", "password"],
                    }
                },
            },
        }
    },
)
async def login(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            credentials = LoginRequest.model_validate(await request.json())
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=exc.errors()) from exc
        email, password = credentials.email, credentials.password
    else:
        # Swagger « Authorize » envoie un formulaire OAuth2 (username + password).
        form = await request.form()
        raw_email = form.get("username") or form.get("email") or ""
        raw_password = form.get("password") or ""
        try:
            credentials = LoginRequest.model_validate({
                "email": str(raw_email),
                "password": str(raw_password),
            })
        except ValidationError as exc:
            raise HTTPException(status_code=422, detail=exc.errors()) from exc
        email, password = credentials.email, credentials.password
    return _token_for_credentials(email, password, db)

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
