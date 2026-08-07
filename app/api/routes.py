from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import get_db, settings
from app.schemas import URLCreate, URLResponse
from app.services import (
    create_short_url,
    get_by_short_code,
)

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

@router.get(
    "/{short_code}",
    status_code=307,
)
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db),
):

    url = get_by_short_code(
        db=db,
        short_code=short_code,
    )

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found.",
        )

    return RedirectResponse(
        url=url.original_url,
    )