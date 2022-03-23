from random import choice, choices, randint
from datetime import datetime
from json import load
from fpdf import FPDF


def print_report_to_pdf(pdf, report):
    """ Function which writes the data from report in pdf file."""
    table_cell_width = 30
    table_cell_height = 5
    pdf.set_font('Times', '', 10)
    column_names = report[0].keys()

    for column in column_names:
        pdf.cell(table_cell_width, table_cell_height, column, align='C', border=1)
    pdf.ln(table_cell_height)
    pdf.set_font('Times', '', 10)

    for line in report:
        for column in column_names:
            if line["Correct answer"] != line["User choice"]:
                pdf.set_font('Times', 'B', 10)
                if column == "Correct answer":
                    pdf.set_text_color(0, 255, 0)
                elif column == "User choice":
                    pdf.set_text_color(255, 0, 0)
                else:
                    pdf.set_text_color(0, 0, 0)
            else:
                pdf.set_font('Times', '', 10)
                pdf.set_text_color(0, 0, 0)
            value = str(line[column])
            if column == 'Letters':
                table_cell_height = 5
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.multi_cell(table_cell_width, table_cell_height, value, align='C', border=1)
                pdf.set_xy(x + table_cell_width, y)
            else:
                table_cell_height = 10
                pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)


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
        """ Generate a pair of random letters."""
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
        """ Generate 4 pairs of letters. """
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
        """ Find the number of matching letter pairs."""
        self.answer = 0
        for index in range(4):
            if self.upper_row[index].lower() == self.lower_row[index].lower():
                self.answer += 1

    def check_answer(self, user_choice):
        """ Check if user has guessed the correct answer. It adds the exercise to the report."""
        self.user_answer = user_choice
        self.add_report()
        if self.answer == self.user_answer:
            return True
        return False

    def add_report(self):
        """ Insert the question with the correct answer and the user's choice
            inside a report list.
        """
        letters = f"{self.upper_row[0]}  {self.upper_row[1]}  {self.upper_row[2]}" \
                  f"  {self.upper_row[3]}\n{self.lower_row[0]}  {self.lower_row[1]}" \
                  f"  {self.lower_row[2]}  {self.lower_row[3]}"
        self.report.append({"Question No": self.questions, "Letters": letters,
                            "Correct answer": self.answer, "User choice": self.user_answer})

    def save_report(self):
        """ Saves the report of this test in a .pdf file. """
        time_now = datetime.now()
        time_format = "%d/%m/%Y %H:%M"
        date_time = time_now.strftime(time_format)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 16)
        pdf.cell(195, 10, 'PERCEPTUAL SPEED TEST REPORT', 0, 1, 'C')
        pdf.cell(195, 10, date_time, 0, 1, 'C')
        pdf.cell(195, 10, f"Score: {self.score}/{self.questions - 1}", 0, 1, 'C')
        pdf.ln(10)

        print_report_to_pdf(pdf, self.report)

        time_format = "%H-%M_%d-%m-%Y"
        date_time = time_now.strftime(time_format)
        pdf.output(f'reports/{date_time}_perceptual_speed_report.pdf', 'F')
