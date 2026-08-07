from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import get_db, settings
from app.schemas import URLCreate, URLResponse
from app.services import create_short_url

router = APIRouter()


@router.post(
    "/shorten",
    response_model=URLResponse,
    status_code=201,
)
def shorten_url(
    request: URLCreate,
    db: Session = Depends(get_db),
):

    url = create_short_url(
        db=db,
        original_url=str(request.original_url),
    )

    return URLResponse(
        original_url=url.original_url,
        short_code=url.short_code,
        short_url=f"{settings.BASE_URL}/{url.short_code}",
    )