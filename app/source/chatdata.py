from dataclasses import dataclass


@dataclass
class ChatData:
    used_answers: dict = None
    state: int = 0

    last_changed: str = None
    route: dict = None

    train: str = None
    time: int = None

    station: str = None
    end_station: str = None

    def reset(self):
        self.used_answers = None
        self.state = 0
        self.last_changed = None
        self.route = None
        self.train = None
        self.time = None
        self.station = None
        self.end_station = None

        return self

