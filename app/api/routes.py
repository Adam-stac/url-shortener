from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.db.database import SessionLocal
from app.repository.url_repository import URLRepository
from app.services.url_service import URLService
from app.schemas.url import URLCreate, URLResponse


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)) -> URLService:
    repo = URLRepository(db)
    return URLService(repo)


@router.post("/shorten", response_model=URLResponse)
def shorten_url(payload: URLCreate, service: URLService = Depends(get_service)):
    url = service.shorten_url(str(payload.url))
    return URLResponse(
        slug=url.slug,
        short_url=f"{settings.base_url}/{url.slug}",
        original_url=url.original_url,
        clicks=url.clicks,
        created_at=url.created_at,
        expires_at=url.expires_at
    )


@router.get("/{slug}")
def redirect_url(slug: str, service: URLService = Depends(get_service)):
    url = service.get_url(slug)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=url.original_url, status_code=307)