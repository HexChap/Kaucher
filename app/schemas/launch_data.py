from pathlib import Path

from pydantic import BaseModel


class LaunchData(BaseModel):
    username: str
    kaboom_dir: Path
    memory: int
    uuid: str
    access_token: str
