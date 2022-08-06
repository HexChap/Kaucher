from pathlib import Path

from pydantic import BaseModel, constr

UUID_PATTERN = TOKEN_PATTERN = r"^[a-fA-F0-9]{8}-([a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}$"


class LaunchData(BaseModel):
    java: Path
    username: str
    kaboom_dir: Path
    memory: int
    uuid: str
    access_token: str


class ModpackLaunchData(LaunchData):
    mp_dir: Path
    version: str
    modpack: str


class LaunchDataPayload(BaseModel):
    user_id: int
    username: str
    access_token: constr(regex=UUID_PATTERN)
    uuid: constr(regex=TOKEN_PATTERN)
