__all__ = ["mes_patterns"]

import random
import typing
from ..source.chatdata import ChatData


# functions
def route_planner(api, data, *args) -> tuple:
    s1 = data.station
    s2 = data.end_station

    route = api.calculate_route(s1, s2)

    if len(route) <= 1:
        return f"After searching I have not found a route from {s1} to {s2}", data

    elif route in ['starting station', 'end station']:
        data.state = 1
        return f"You have not told me your {route} yet.\nJust type the name here:", data

    elif route in ['starting', 'end']:
        return f"I could not locate {route} station for you", data

    else:
        data.route = route

        def _gen():
            for i, x in enumerate(l := list(route.items())):
                if x[1] is not None:
                    yield f'{x[0]} (with {x[1]}) → {l[i + 1][0]}'

        return random.choice([
            "This is the shortest route I found:",
            "I found the following route:",
            "The best route I could find for you:"
        ]) + "\n" + "\n".join(_gen()), data


def show_route(api, data, *args) -> tuple:
    s = data.station
    route = api.get_line(s, data.train)

    if route is None:
        return f"I could not find the train \"{data.train}\" in {s}", data

    elif route == "no line":
        data.state = 2
        return f"You have not specified a trainline yet.\nEnter one below:", data

    elif route == "starting station":
        data.state = 1
        return f"I need to know a station your train stops at.\nJust type the name here:", data

    elif route == "starting":
        return f"I cannot find the station {data.station}", data

    else:
        return random.choice([
            f"{data.train} stops at these stations:",
            f"At these stations does {data.train} stop:",
        ]) + "\n" + ", ".join(route) + \
               "\n\nIf you need me to find a route between two stations just ask me", data


def show_depart(api, data, *args) -> tuple:
    s = data.station
    lines = api.get_departing(s)

    if lines == "starting station":
        data.state = 1
        return f"Which station should I look up?\nJust type the name here:", data

    elif lines == "starting":
        return f"I cannot find the station {data.station}", data

    else:
        return random.choice([
            f'These trains will leave {s} in the current hour:',
            f'I found these trains leaving {s} in this hour:'
        ]) + "\n" + "\n".join(lines), data


# returns a text
mes_patterns: list[tuple[str, typing.Callable]] = [
    (
        r"what(.)*you(.)*(do|purpose|job)",
        lambda api, data, *args: (
            random.choice([
                "I can answer Questions about German trains or stations.",
                "Help you with Questions on German trains or stations."
            ]) + "\nYou can for example ask me about a route, check the train stops for a "
                 "line or show the departing trains from a station"
            , data
        )
    ),
    (
        r"(route|travel|get|go)?\s(.)*?(from|to)",
        route_planner
    ),
    (
        r"(show)(.)*(line|train)",
        show_route
    ),
    (
        r"(which|trains)(.)*(depart|leave)(.)*",
        show_depart
    ),
    (
        r"(.)*?(travel)?(.)*(options)(.)*",
        show_depart
    ),
    (
        r"(.)*(buy|sell)?(.)*(tickets)",
        lambda api, data, *args: (
            random.choice([
                "I sadly cannot do that. Please visit the tickets page to buy tickets",
                "I am not able to buy you tickets. Please visit the ticket page",
                "I cannot sell tickets. Please check the ticket page for more information"
            ]),
            data
        )
    ),
    (
        r"(tell|show)(.)*(more)",
        lambda api, data, *args: (
            random.choice([
                "I cannot show you more because I cannot access more data",
                "I would show more but I cant access more data"
            ])
            , data
        )
    ),
    (
        r"((who)(.*)(you)|(you)(.*)(name))",
        lambda api, data, *args: (
            random.choice([
                "My name is Bob and I am here to help you",
                "I am Bob. What can I help you with?"
            ]) + "\nAsk me about a train fact!"
            , data
        )
    ),
    (
        r"(train)(.*)(fact)",
        lambda api, data, *args: (
            random.choice([
                "A Siemens electric train needs about 11s to get to 100km/h",
                "You can travel to Sylt via Train. The route has been built 1927/1928",
                "A Train is only late when it arrives at least 6 minutes late.",
                "The first train in Germany started operating on the 07.12.1835",
                "Every third ICE train is behind schedule",
                "Over 200.000 people work for the DB company in Germany",
                "The most heavily used bridge by trains is the Hohenzollern Brücke"
            ])
            , data
        )
    ),
    (
        r"(hi|hello|help)",
        lambda api, data, *args: (
            random.choice([
                "Hello! How may I help you today?",
                "Good day! How can I help?",
                "Hi! I am here to help!"
            ]) + "\nAsk me about what I can do for more information"
            , data
        )
    ),
    (
        "(quit|reset|stop|bye|leave)",
        lambda api, data, *args: (
            random.choice([
                "See you later my friend! I hope I could help you",
                "Bye! I hope I was able to answer your questions",
                "See you! I hope my answers answered your questions"
            ])
            , ChatData()
        )
    )
]
