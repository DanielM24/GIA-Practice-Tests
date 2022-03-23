from random import sample, randint, shuffle


class SpatialVisualisation:
    def __init__(self):
        self.picture_angles = [(0, 0), (0, 90), (0, 180), (0, 270), (1, 0), (1, 90), (1, 180), (1, 270)]
        self.answer = None
        self.user_answer = None
        self.pairs = None
        self.questions = 0
        self.score = 0

    def get_non_matching_r(self):
        while True:
            pair = sample(self.picture_angles, 2)
            if pair[0][0] != pair[1][0]:
                return pair

    def get_matching_r(self):
        while True:
            pair = sample(self.picture_angles, 2)
            if pair[0][0] == pair[1][0] and pair[0] != pair[1]:
                return pair

    def get_pairs(self):
        self.answer = randint(0, 2)
        self.questions += 1
        self.pairs = []
        if self.answer == 0:
            while len(self.pairs) < 2:
                pair = self.get_non_matching_r()
                if pair not in self.pairs:
                    self.pairs.append(pair)

        elif self.answer == 1:
            self.pairs.append(self.get_matching_r())
            self.pairs.append(self.get_non_matching_r())
            shuffle(self.pairs)

        elif self.answer == 2:
            while len(self.pairs) < 2:
                pair = self.get_matching_r()
                if pair not in self.pairs:
                    self.pairs.append(pair)

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
