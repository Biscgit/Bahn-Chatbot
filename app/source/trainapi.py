import logging
import tomllib
import typing
import math
import threading

from deutsche_bahn_api.api_authentication import ApiAuthentication
from deutsche_bahn_api.station_helper import StationHelper, Station
from deutsche_bahn_api.timetable_helper import TimetableHelper, Train

__all__ = ['TrainAPI']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TrainAPI(ApiAuthentication):
    def __init__(self):
        with open("config/DBapi.toml", "rb") as file:
            data = tomllib.load(file)['DBApi']

        super().__init__(data['api_id'], data['api_key'])

        if not self.test_credentials():
            print("Failed to authenticate DB Api")
            exit(-127)

        self.stations = StationHelper()
        self.stations.load_stations()
        logger.info("TrainAPI setup")

    def calculate_route(self, s: str, e: str):
        if s is None:
            return "starting station"

        if e is None:
            return "end station"

        try:
            start: Station = self.get_station_names(s)[0]
        except IndexError:
            return "starting"

        try:
            destination: Station = self.get_station_names(e)[0]
        except IndexError:
            return "end"

        visited_stations: dict[str: int] = {}
        fastest_path = {}

        length_factor = 1.2
        total_max_distance = self.calculate_station_distance(start, destination) * length_factor + 50
        print(f'{total_max_distance = }')

        def _execute(s: Station, used_trains: dict[str, str], max_distance: float) -> None:
            nonlocal fastest_path

            # stop if found
            if fastest_path:
                return

            # return if already processed except if shorter path found
            if hops := visited_stations.get(s.NAME):
                # shorter path already exists
                if hops <= len(used_trains):
                    return

            visited_stations.update({s.NAME: len(used_trains)})

            for train in self.get_time_tables(s, None):
                # no busses
                if (train_name := self.train_name(train)) in used_trains.values() \
                        or train_name.lower().startswith("bus"):
                    continue

                # adding all stations on the plan except local
                reachable_stations = train.stations.split('|')
                if hasattr(train, "passed_stations"):
                    reachable_stations.extend(train.passed_stations.split('|'))

                if destination.NAME in reachable_stations:
                    fastest_path = used_trains | {s.NAME: train_name}
                    return

                # sort out not found stations and stations that are too far away
                station_distance = {
                    y[0]: dist for x in reachable_stations
                    if (y := self.get_station_names(x)) and
                       (dist := self.calculate_station_distance(y[0], destination)) <
                       min(max_distance * length_factor + 50, total_max_distance)
                }

                reachable_stations = sorted(
                    station_distance.keys(),
                    key=lambda x: station_distance[x]
                )

                # max recursion level: 3
                if len(used_trains.keys()) >= 3:
                    return

                threads = []

                for stat in reachable_stations:
                    thread = threading.Thread(
                        target=_execute,
                        args=(
                            stat,
                            used_trains | {s.NAME: train_name},
                            station_distance[stat],
                        )
                    )
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

        _execute(start, {}, total_max_distance)
        return fastest_path | {destination.NAME: None}

    def get_line(self, s, name):
        if s is None:
            return "starting station"

        if name is None:
            return "no line"

        try:
            station: Station = self.get_station_names(s)[0]
        except IndexError:
            return "starting"

        table = self.get_time_tables(station)

        def check(t: Train) -> bool:
            if name.lower() == self.train_name(t).lower():
                return True

            return name == t.train_number

        table.sort(key=lambda x: x.departure)
        try:
            train = [train for train in table if check(train)][0]
        except IndexError:
            return None

        stations = ((train.passed_stations + '|') if hasattr(train, "passed_stations") else "") \
                   + f"{station.NAME}|" + train.stations

        return stations.split('|')

    def get_departing(self, s):
        if s is None:
            return "starting station"

        try:
            station: Station = self.get_station_names(s)[0]
        except IndexError:
            return "starting"

        table = self.get_time_tables(station)

        def get_train_info(t: Train) -> str:
            line = self.train_name(t, force_id=True)

            time = f"{t.departure[-4:-2]}:{t.departure[-2:]}"
            destination = f"{t.stations.split('|')[-1]}"

            return f"[{time}] {line} to {destination}"

        table.sort(key=lambda x: x.departure)
        routes = [get_train_info(train) for train in table]

        return routes

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @staticmethod
    def train_name(t: Train, force_id: bool = False) -> str:
        return "".join([
            t.train_type,
            f"{t.train_line}{f'({t.train_number})' if force_id else ''}"
            if hasattr(t, "train_line")
            else f"{t.train_number}"
        ])

    def get_station_names(self, name: str, matches: int = None) -> list[Station]:
        return self.stations.find_stations_by_name(name)

    def get_time_tables(self, station: Station, time: typing.Optional[int] = None) -> list[Train]:
        tables = TimetableHelper(station, self)
        return tables.get_timetable(None)

    @staticmethod
    def calculate_station_distance(s1: Station, s2: Station) -> float:
        # earth radius
        radius = 6371

        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(float(s1.Breite.replace(',', '.')))
        lon1_rad = math.radians(float(s1.Laenge.replace(',', '.')))
        lat2_rad = math.radians(float(s2.Breite.replace(',', '.')))
        lon2_rad = math.radians(float(s2.Laenge.replace(',', '.')))

        # Calculate the differences between coordinates
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        # Haversine formula
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Calculate the distance
        return abs(radius * c)
