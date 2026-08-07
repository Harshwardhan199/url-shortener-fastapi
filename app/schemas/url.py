from pydantic import BaseModel, HttpUrl, ConfigDict


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    original_url: HttpUrl
    short_code: str
    short_url: str

    model_config = ConfigDict(from_attributes=True)