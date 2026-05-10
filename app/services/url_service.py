from app.repository.url_repository import URLRepository
from app.db.models import URL


BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    result = []
    while num > 0:
        result.append(BASE62[num % 62])
        num //= 62
    return "".join(reversed(result))


class URLService:

    def __init__(self, repo: URLRepository):
        self.repo = repo

    def shorten_url(self, original_url: str) -> URL:
        existing = self.repo.get_by_original_url(original_url)
        if existing:
            return existing

        db_url = self.repo.create(original_url)
        slug = encode_base62(db_url.id)
        return self.repo.update_slug(db_url, slug)

    def get_url(self, slug: str) -> URL | None:
        db_url = self.repo.get_by_slug(slug)
        if db_url:
            self.repo.increment_clicks(db_url)
        return db_url