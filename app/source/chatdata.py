from dataclasses import dataclass


@dataclass
class ChatData:
    state: int = 0

    last_changed: str = None
    route: dict = None

    train: str = None
    time: int = None

    station: str = None
    end_station: str = None
