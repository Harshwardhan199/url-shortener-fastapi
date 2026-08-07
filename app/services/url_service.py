from sqlalchemy.orm import Session

from app.models import URL
from app.services.shortener import generate_short_code


def get_by_short_code(
    db: Session,
    short_code: str,
) -> URL | None:
    return (
        db.query(URL)
        .filter(URL.short_code == short_code)
        .first()
    )


def create_short_url(
    db: Session,
    original_url: str,
) -> URL:

    for _ in range(5):

        short_code = generate_short_code()

        existing = get_by_short_code(
            db,
            short_code,
        )

        if existing:
            continue

        url = URL(
            original_url=original_url,
            short_code=short_code,
        )

        db.add(url)
        db.commit()
        db.refresh(url)

        return url

    raise RuntimeError(
        "Unable to generate unique short code."
    )