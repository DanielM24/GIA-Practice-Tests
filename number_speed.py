from random import sample, shuffle
# from datetime import datetime


class NumberSpeedAccuracy:
    def __init__(self):
        self.numbers = []
        self.report = []
        self.answer = 0
        self.user_answer = 0
        self.score = 0

    def get_numbers(self):
        """ Generate a list of 3 numbers following these rules:
            - The difference between the SMALLEST number and the LARGEST number is max 10;
            - The difference between any 2 numbers is min 2;
            - The difference between 2 numbers can't be the same.
        """
        self.numbers = []
        self.numbers = sorted(sample(range(2, 30), 3))
        while self.numbers[2] - self.numbers[0] > 10 \
                or self.numbers[2] - self.numbers[1] < 2 \
                or self.numbers[1] - self.numbers[0] < 2 \
                or self.numbers[2] - self.numbers[1] == self.numbers[1] - self.numbers[0]:
            self.numbers = sorted(sample(range(2, 30), 3))
        shuffle(self.numbers)

    def find_answer(self):
        """ Find whether the largest or the smallest number from the list
            is further away from the remaining number.
        """
        numbers = sorted(self.numbers)
        if numbers[2] - numbers[1] > numbers[1] - numbers[0]:
            self.answer = numbers[2]
        else:
            self.answer = numbers[0]

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
        self.report.append(f"Numbers: {self.numbers}, Correct answer: {self.answer}, User choice: {self.user_answer}")

    def save_report(self):
        """ Saves the report of this exercise in a .pdf format """
        pass
