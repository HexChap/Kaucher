from pydantic import BaseModel


class APIInfo(BaseModel):
    api_version: str
    build_version: str
