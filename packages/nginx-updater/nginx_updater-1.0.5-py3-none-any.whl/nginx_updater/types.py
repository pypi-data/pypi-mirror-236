from typing import List
from typing import Optional
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
    scp_executable: Optional[str]
    scp_destination: Optional[str]
