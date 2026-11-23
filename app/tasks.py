from app.celery_app import celery
from app.db.session import SessionLocal
from app.models import Notification

@celery.task(name="app.tasks.create_project_notification")
def create_project_notification(user_id: int, project_name: str):
    """Persist an in-app notification asynchronously after a project is created."""
    db = SessionLocal()
    try:
        notification = Notification(user_id=user_id, message=f'Проект «{project_name}» успешно создан')
        db.add(notification)
        db.commit()
        return {"notification_id": notification.id, "user_id": user_id}
    finally:
        db.close()
