from json import load
from random import sample, choice, randint


class Reasoning:
    def __init__(self):
        self.people = ["Josh", "Thomas", "Ben", "Jack", "Greg", "Sam", "Lily", "Rachel", "Anna", "Jasmine"]
        self.adverbs = ['is not as', 'is']
        self.phrase = ""
        self.question = ""
        self.person_1 = ""
        self.person_2 = ""
        self.adverb = ""
        self.adjective = ""
        self.user_answer = ""
        self.answer = ""
        self.situation = 0
        self.score = 0
        with open('resources/adjectives.json') as adjectives_file:
            self.adjectives = load(adjectives_file)

    def get_phrase(self):
        self.person_1, self.person_2 = sample(self.people, 2)
        self.adjective = choice(self.adjectives)
        self.adverb = choice(self.adverbs)

        if self.adverb == 'is':
            self.phrase = f"{self.person_1} {self.adverb} {self.adjective['comparative']} than {self.person_2}."
        elif self.adverb == 'is not as':
            self.phrase = f"{self.person_1} {self.adverb} {self.adjective['adjective']} as {self.person_2}."

    def get_question(self):
        self.situation = randint(0, 1)
        if self.situation == 0:
            self.question = f"Who is {self.adjective['antonym']}?"
        elif self.situation == 1:
            self.question = f"Who is {self.adjective['comparative']}?"

    def find_answer(self):
        if self.adverb == 'is':
            if self.situation == 0:
                self.answer = self.person_2
            else:
                self.answer = self.person_1
        elif self.adverb == 'is not as':
            if self.situation == 0:
                self.answer = self.person_1
            else:
                self.answer = self.person_2

    def check_answer(self, user_choice):
        """ Check if user has guessed the correct answer."""
        self.user_answer = user_choice
        if self.answer == self.user_answer:
            return True
        return False

    def add_report(self):
        """ Insert the question with the correct answer and the user's choice
            inside a report list which can be later saved
        """
        pass

    def save_report(self):
        """ Saves the report of this exercise in a .pdf format """
        pass
