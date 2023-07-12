__all__ = ["mes_patterns"]

import typing

"""regex patterns that generate an answer via a function.
This can be expanded via the pattern below"""
from .processing import *


# returns a text
mes_patterns: list[tuple[str, typing.Callable]] = [
    (
        r"\b(route|travel|get|go)\s\b(.)*?(from|to|between)",
        route_planner
    ),
    (
        r"(show)(.*)(line|train|stop|station|route)",
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
        r"(how\sfar|distance)",
        show_distance
    ),
    (
        r"(do|is)(.)*hot?(\s)?(line)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "This is their phone-number:\n030-2970\nYou can call them if you have any issues",
                "You can reach the hotline with 030-2970",
                "The DB phone service hotline is reachable with 030-2970"
            ])
        )
    ),
    (
        r"(.)*(buy|sell)?(.)*(tickets)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "I sadly cannot do that. Please visit the tickets page to buy tickets",
                "I am not able to buy you tickets. Please visit the ticket page",
                "I cannot sell tickets. Please check the ticket page for more information"
            ])
        )
    ),
    (
        r"(tell|show)(.)*(more)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "I cannot show you more because I cannot access more data",
                "I would show more but sadly I cannot access more data",
                "The access I have is limited. This is all I can show"
            ])
        )
    ),
    (
        r"what(.)*you(.)*(do|purpose|job)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "I can answer Questions about German train routes or stations.",
                "I can give you random train facts or show a route",
                "I can check departing trains from a station or calculate the distance"
            ]) + "\nYou can for example ask me about a route, check the train stops for a "
                 "line or show the departing trains from a station"
        )
    ),
    (
        r"((who)(.*)(you)|(you)(.*)(name))",
        lambda api, data, *args: (
            choice_cacher(data, [
                "My name is Bob and I am here to help you",
                "I am Bob. What can I help you with?",
                "This is Bob and I am ready to help!"
            ]) + "\nAsk me about a train fact!"
        )
    ),
    (
        r"(train)(.*)(fact)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "A Siemens electric train needs about 11s to get to 100km/h",
                "You can travel to Sylt via Train. The route has been built in 1927/1928",
                "A Train is only late when it arrives at least 6 minutes late.",
                "The first train in Germany started operating on the 07.12.1835",
                "Every third ICE train is behind schedule",
                "Over 200.000 people work for the DB company in Germany",
                "The most heavily used bridge by trains is the Hohenzollern Brücke"
            ])
        )
    ),
    (
        r"(is|will)(.)*(late|on time)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "DB does not allow me to access that information. You should check their site "
                "weather your train is on time or late",
                "I do not have access to delayed trains, so sadly I cannot tell you",
                "Please check the DB website because I cannot access that information"
            ])
        )
    ),
    (
        r"(hi|hello|help)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "Hello! How may I help you today?",
                "Good day! How can I help?",
                "Hi! I am here to help!"
            ]) + "\nAsk me about what I can do for more information"
        )
    ),
    (
        r"(bring|take)?(.*)(dog|animal|cat|pet)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "You can bring small animals with you.",
                "It is possible to take small dogs with you, but you need to buy "
                "a ticket for larger ones.",
                "Small pets can travel for free, while bigger pets need their own train ticket."
            ]) + "\nNote that service animals are always free when wearing appropriate accessory"
        )
    ),
    (
        r"(can|possible|allowed)?(.*)(smoke|cigarettes)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "Smoking on trains is strictly prohibited",
                "It is allowed in certain areas at train stations but not on the train",
                "No, you can only smoke in marked areas at stations"
            ])
        )
    ),
    (
        r"(thank you|thanks)",
        lambda api, data, *args: (
            choice_cacher(data, [
                "You are welcome! If you need any help I am here",
                "Sure! Let me know if you need anything else",
                "Thank you! I am here if you need anything"
            ])
        )
    ),
    (
        r"(quit|reset|stop|bye|leave|clear)",
        lambda api, data, *args: (
            choice_cacher(data.reset(), [
                "See you later my friend! I hope I could help you",
                "Bye! I hope I was able to answer your questions",
                "See you! I hope my answers answered your questions"
            ])
        )
    )
]
