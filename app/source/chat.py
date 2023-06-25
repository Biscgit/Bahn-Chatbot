import copy
import string
import nltk

from app import message_patterns, memory_patterns
from app.source.chatdata import ChatData
from .trainapi import TrainAPI
from ..language.processing import choice_cacher


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

API = TrainAPI()


class Chat(object):
    def __init__(self, user_id: str):
        self._id = user_id

        # 0: input, >0: waiting for data
        self._missing: list = []
        self._data: ChatData = ChatData()

        self._asked_questions = []

    @staticmethod
    def remove_punctuation(text):
        translator = str.maketrans("", "", string.punctuation)
        return text.translate(translator)

    def chatbot_response(self, message: str) -> str:
        before_data = copy.deepcopy(self._data)

        if message is None:
            return "502 Internal Error, no message provided"

        message: str = self.remove_punctuation(message)

        if message in self._asked_questions and self._data.state == 0:
            return choice_cacher(self._data, [
                "You have already asked me this question",
                "There are also other questions you can ask me",
                "You can ask me other things too!"
            ])

        # more input states
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

        # cant be handles by message interpretation
        original_message = message
        if len(x := message.split(' at ', maxsplit=1)) > 1:
            message = f'at {x[1]} {x[0]}'

        # message analyzing
        for pattern, answer_function in memory_patterns:
            match = nltk.re.search(pattern, message, flags=nltk.re.IGNORECASE)
            if match:
                groups = match.groups()
                self._data = answer_function(self._data, *groups)

        if original_message.startswith(("and", "to")) and len(self._asked_questions) >= 2:
            self._asked_questions.pop(-1)
            message = self._asked_questions[-1]

        for pattern, answer_function in message_patterns:
            match = nltk.re.search(pattern, message, flags=nltk.re.IGNORECASE)
            if match:
                return answer_function(API, self._data)

        after_data = copy.deepcopy(self._data)
        after_data.used_answers = None
        before_data.used_answers = None

        if before_data == after_data:
            return choice_cacher(self._data, [
                "Could you rephrase that please? I do not understand",
                "I do not understand what you are trying to say",
                "Try to be more specific with what you say, I do not understand",
                "I do not have an answer to that",
                "Please say it again with different words because I do not understand"
            ])

        else:
            return choice_cacher(self._data, [
                "I will remember that information",
                "Thank you, I will remember this for your next questions",
                "I will save that for your questions later",
                "Thank you for providing more detailed information"
            ])
