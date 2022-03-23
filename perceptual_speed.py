from json import load
from random import choice, choices, randint


class PerceptualSpeed:
    def __init__(self):
        with open('resources/letters.json') as letters_file:
            self.letters = load(letters_file)
        self.upper_row = []
        self.lower_row = []
        self.report = []
        self.questions = 0
        self.answer = 0
        self.user_answer = 0
        self.score = 0

    def choice_letters(self):
        letter = choice(list(self.letters.keys()))
        letter_weights = [1 for _ in range(0, len(list(self.letters.keys())))]
        for character in self.letters[letter]:
            index = list(self.letters.keys()).index(character)
            letter_weights[index] += 19
        letter_weights[list(self.letters.keys()).index(letter)] += 34
        pair_letter = choices(list(self.letters.keys()), weights=letter_weights, k=1)
        # print(letter, pair_letter[0])
        return [letter, pair_letter[0]]

    def get_letters(self):
        self.upper_row = []
        self.lower_row = []
        while len(self.upper_row) < 4:
            pair = self.choice_letters()
            if pair[0] not in self.upper_row and pair[1] not in self.lower_row:
                self.upper_row.append(pair[0])
                self.lower_row.append(pair[1])
        self.questions += 1
        if randint(0, 1) == 0:
            self.upper_row = [letter.upper() for letter in self.upper_row]
        else:
            self.lower_row = [letter.upper() for letter in self.lower_row]

    def find_answer(self):
        self.answer = 0
        for index in range(4):
            if self.upper_row[index].lower() == self.lower_row[index].lower():
                self.answer += 1

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
