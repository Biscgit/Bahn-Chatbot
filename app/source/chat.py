import copy
import logging
import string
import nltk

from app import message_patterns, memory_patterns
from app.source.chatdata import ChatData
from .trainapi import TrainAPI
from ..language.processing import choice_cacher

# download needed natural language libraries
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# single api instance
API = TrainAPI()


class Chat(object):
    """Chat containing data for every connection"""

    def __init__(self, user_id: str):
        self._id = user_id

        # 0: input, >= 1: waiting for data
        self._missing: list = []
        self._data: ChatData = ChatData()

        self._asked_questions = []

    @staticmethod
    def remove_punctuation(text):
        translator = str.maketrans("", "", string.punctuation)
        return text.translate(translator)

    def chatbot_response(self, message: str) -> str:
        """Function which takes the input message and generates one based on the input
        and past conversation data."""

        # formatting message and checks
        before_data = copy.deepcopy(self._data)

        if message is None:
            return "502 Internal Error, no message provided"

        message: str = self.remove_punctuation(message)

        # check if question already asked
        if message in self._asked_questions and self._data.state == 0:
            return choice_cacher(self._data, [
                "You have already asked me this question",
                "There are also other questions you can ask me",
                "You can ask me other things too!"
            ])

        # input states for adding needed information (1: station, 2: train), resets state after input
        if self._data.state > 0:
            if self._data.state == 1:
                if self._data.station:
                    self._data.end_station = message
                else:
                    self._data.station = message

            elif self._data.state == 2:
                self._data.train = message

            self._data.state = 0
            message = self._asked_questions[-1]

        else:
            self._asked_questions.append(message)

        # at cant be handled by message interpretation: quick fix
        original_message = message
        if len(x := message.split(' at ', maxsplit=1)) > 1:
            message = f'at {x[1]} {x[0]}'

        # message analyzing: chat memory
        for pattern, answer_function in memory_patterns:
            match = nltk.re.search(pattern, message, flags=nltk.re.IGNORECASE)

            if match:
                groups = match.groups()
                self._data = answer_function(self._data, *groups)

        # "continuing" the last message
        if original_message.startswith(("and", "to", "another")) and len(self._asked_questions) >= 2:
            self._asked_questions.pop(-1)
            message = self._asked_questions[-1]

        # message analyzing: chat action
        for pattern, answer_function in message_patterns:
            if match := nltk.re.search(pattern, message, flags=nltk.re.IGNORECASE):
                try:
                    print(f'First valid pattern: {pattern}')
                    return answer_function(API, self._data, match.groups())

                except Exception as e:
                    logging.error(f'Error in message generation: {e}')
                    return "Internal Server Exception 500"

        print(f'No valid pattern found')

        # on unrecognized message pattern: use the last valid message for next call
        if len(self._asked_questions) >= 1:
            self._asked_questions.pop(-1)

        # answer depending on if information has been updated
        after_data = copy.deepcopy(self._data)
        after_data.used_answers = None
        before_data.used_answers = None

        if before_data == after_data:
            # provides questions if nothing got recognized -> chat interaction
            return choice_cacher(self._data, [
                "Could you rephrase that please? I do not understand",
                "I do not understand what you are trying to say",
                "Try to be more specific with what you say, I do not understand",
                "I do not have an answer to that",
                "Please say it again with different words because I do not understand"
            ]) + "\n" + choice_cacher(self._data, [
                "Maybe ask about a train route",
                "You can ask me about departing trains instead",
                "I can give you a random train fact!",
                "If you need the hotline just let me know"
            ])

        else:
            return choice_cacher(self._data, [
                "I will remember that information",
                "Thank you, I will remember this for your next questions",
                "I will save that for your questions later",
                "Thank you for providing more detailed information"
            ])
