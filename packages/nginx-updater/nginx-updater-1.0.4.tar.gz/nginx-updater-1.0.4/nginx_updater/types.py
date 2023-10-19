from typing import List
from typing import TypedDict


class Config(TypedDict):
    name: str
    url: str
    username: str
    password: str
    file_path: str
    extract_dir: str
    exclude: List[str]
    packages: List[str]
    scp_executable: str
    scp_destination: str
