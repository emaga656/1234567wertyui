from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Notification, User
from app.core.deps import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("")
def list_notifications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.id.desc()).all()
    return [{"id": n.id, "message": n.message, "created_at": n.created_at} for n in rows]
