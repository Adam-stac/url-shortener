from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    # HttpUrl validates the input is a real URL, not just any string.
    # Pydantic rejects invalid URLs before they reach the service layer.
    url: HttpUrl

class URLResponse(BaseModel):
    slug: str
    short_url: str
    original_url: str
    clicks: int
    created_at: datetime
    expires_at: Optional[datetime] = None

    # Allows Pydantic to read directly from SQLAlchemy model instances.
    # Without this, database rows would need manual conversion to dicts first.
    model_config = {"from_attributes": True}