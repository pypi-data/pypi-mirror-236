from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class PlatformEnum(str, Enum):
    """Simple enum listing options for platform_type attribute in Session dataclass/validation schema."""

    CLOUD = "cloud"
    DESKTOP = "desktop"


@dataclass
class Session:
    user_uid: str
    auth0_session_id: str  #auth0 response - session_id
    platform_type: PlatformEnum  #cloud or desktop
    version: Optional[str] = None  #forloop platform version
    ip: Optional[str] = None  # only in desktop/execution core version
    mac_address: Optional[str] = None  # only in desktop/execution core version
    hostname: Optional[str] = None  # only in desktop/execution core version
    start_datetime_utc: datetime = datetime.utcnow()
    last_datetime_utc: datetime = datetime.utcnow()
    total_time: int = 0
    uid: Optional[str] = None