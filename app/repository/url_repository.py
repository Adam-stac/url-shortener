from sqlalchemy.orm import Session
from app.db.models import URL


class URLRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str) -> URL | None:
        return self.db.query(URL).filter(URL.slug == slug).first()

    def get_by_original_url(self, original_url: str) -> URL | None:
        return self.db.query(URL).filter(URL.original_url == original_url).first()

    # flush sends the pending INSERT to PostgreSQL within the open transaction
    # without committing — PostgreSQL assigns the id so we can encode it to Base62
    def create(self, original_url: str) -> URL:
        db_url = URL(original_url=original_url)
        self.db.add(db_url)
        self.db.flush()
        return db_url

    # refresh reloads the instance from the database after commit
    # ensures server-generated values like created_at are populated
    def update_slug(self, db_url: URL, slug: str) -> URL:
        db_url.slug = slug
        self.db.commit()
        self.db.refresh(db_url)
        return db_url

    def increment_clicks(self, db_url: URL) -> None:
        db_url.clicks += 1
        self.db.commit()