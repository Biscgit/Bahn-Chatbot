import random
import string
import nltk

from app import message_patterns, memory_patterns
from app.source.chatdata import ChatData
from .trainapi import TrainAPI

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class Chat(object):
    api = TrainAPI()

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
        before_data = self._data

        if message is None:
            return "502 Internal Error, no message provided"

        message: str = self.remove_punctuation(message)

        if message in self._asked_questions and self._data.state == 0:
            return random.choice([
                "You have already asked me this question",
                "There are also other questions you can ask me",
                "You can ask me other things too!"
            ])

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

        for pattern, answer_function in memory_patterns:
            match = nltk.re.search(pattern, message, flags=nltk.re.IGNORECASE)
            if match:
                groups = match.groups()
                self._data = answer_function(self._data, *groups)

        if message.startswith(("and", "to")) and len(self._asked_questions) >= 2:
            self._asked_questions.pop(-1)
            message = self._asked_questions[-1]

        for pattern, answer_function in message_patterns:
            match = nltk.re.search(pattern, message, flags=nltk.re.IGNORECASE)
            if match:
                mes, self._data = answer_function(self.api, self._data)
                return mes

        if before_data == self._data:
            return "I'm sorry, I don't have an answer for that question."

        else:
            return "I updated additional information!"


a = Chat("")
