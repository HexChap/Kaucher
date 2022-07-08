from pathlib import Path

from pydantic import BaseModel


class LaunchData(BaseModel):
    username: str
    game_dir: Path
    uuid: str
    access_token: str
