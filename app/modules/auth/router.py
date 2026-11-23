from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user
from app.modules.auth.schemas import RegisterIn, UserOut, TokenOut
from app.core.config import settings
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post("/register", response_model=UserOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password), role="user")
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=TokenOut)
@limiter.limit(settings.rate_limit_login)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    return TokenOut(access_token=create_access_token(str(user.id)))

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
