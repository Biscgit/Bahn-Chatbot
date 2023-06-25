import random


def choice_cacher(data, options: list[str]) -> str:
    level = 3

    if data.used_answers is None:
        data.used_answers = {}

    matches = {k: data.used_answers.get(k, 0) for k in options}
    options = list(matches.keys())
    weights = [round(1 / (x + 1), 4) for x in matches.values()]

    choice = random.choices(options, weights=weights)[0]
    data.used_answers.update({choice: (matches.get(choice) + level)})

    return choice


def route_planner(api, data, *args) -> str:
    s1 = data.station
    s2 = data.end_station
    time = data.time

    route = api.calculate_route(s1, s2, time)

    if len(route) <= 1:
        return choice_cacher(data, [
            "I searched but I cannot find a route",
            "I looked up a lot of routes but I cannot find one",
            "After searching I sadly cannot find a route"
        ]) + f" from {s1} to {s2}" + (f" at {time % 12}{'pm' if time // 12 else 'am'}" if time else "")

    elif route in ['starting station', 'end station']:
        data.state = 1
        return f"You have not told me your {route} yet.\n" + choice_cacher(data, [
            "Just type the name here:",
            "Enter it here without anything else:",
            "Type it here so I can look it up:"
        ])

    elif route in ['starting', 'end']:
        return f"I could not locate {route} station for you" + choice_cacher(data, [
            "You can ask me again with a different station",
            "If you want to change stations you can just ask me again"
        ])

    else:
        data.route = route

        def _gen():
            for i, x in enumerate(l := list(route.items())):
                if x[1] is not None:
                    yield f'{x[0]} (with {x[1]}) → {l[i + 1][0]}'

        return choice_cacher(data, [
            "This is the shortest route I found:",
            "I found the following route:",
            "The best route I could find for you:"
        ]) + "\n" + "\n".join(_gen())


def show_route(api, data, *args) -> str:
    s = data.station
    route = api.get_line(s, data.train)

    if route is None:
        return f"I could not find the train \"{data.train}\" in {s}"

    elif route == "no line":
        data.state = 2
        return f"You have not specified a trainline yet.\n" + choice_cacher(data, [
            "Just type the name here:",
            "Enter it here without anything else:",
            "Type it here so I can look it up:"
        ])

    elif route == "starting station":
        data.state = 1
        return f"I need to know a station your train stops at.\n" + choice_cacher(data, [
            "Just type the name here:",
            "Enter it here without anything else:",
            "Type it here so I can look it up:"
        ])

    elif route == "starting":
        return choice_cacher(data, [
            "I cannot find the station",
            "I failed to find your entered station",
            "I cannot locate your requested station"
        ]) + f" {data.station}"

    else:
        return f"{data.train} " + choice_cacher(data, [
            "has following stops:",
            "stops at the stations listed below:",
            "stops at these stations:"
        ]) + "\n- " + "\n- ".join(route)


def show_depart(api, data, *args) -> str:
    s = data.station
    time = data.time
    lines = api.get_departing(s, time)

    if lines == "starting station":
        data.state = 1
        return f"Which station should I look up?\n" + choice_cacher(data, [
            "Just type the name here:",
            "Enter it here without anything else:",
            "Type it here so I can look it up:"
        ])

    elif lines == "starting":
        return choice_cacher(data, [
            "I cannot find the station",
            "I failed to find your entered station",
            "I cannot locate your requested station"
        ]) + f" {data.station}"

    else:
        return choice_cacher(data, [
            'These trains will leave',
            'I found these trains leaving',
            'Following trains will leave'
        ]) + f" {s} " + (f"at {time % 12}{'pm' if time // 12 else 'am'}\n" if time \
            else 'this hour:\n') + "\n".join(lines)


def show_distance(api, data, *args) -> str:
    s1 = data.station
    s2 = data.end_station

    distance = api.get_distance(s1, s2)

    if distance in ['starting station', 'end station']:
        data.state = 1
        return f"You have not told me your {distance} yet.\n" + choice_cacher(data, [
            "Just type the name here:",
            "Enter it here without anything else:",
            "Type it here so I can look it up:"
        ])

    elif distance in ['starting', 'end']:
        data.state = 1
        return f"I could not locate the {distance} station for you.\n" + choice_cacher(data, [
            "Just type the name here:",
            "Enter it here without anything else:",
            "Type it here so I can look it up:"
        ])

    else:
        distance = round(distance, 1)
        return random.choice([
            f"{s1} is {distance}km away from {s2}",
            f"The distance between {s1} and {s2} is {distance}km",
            f"You need to travel about {distance}km from {s1} to {s2}"
        ])
