from random import sample, choice, randint
from datetime import datetime
from json import load
from fpdf import FPDF


def cell_width(cell_name):
    """ Set the width of the cells from the pdf report file."""
    if cell_name == "No":
        table_cell_width = 6
    elif cell_name == "Phrase":
        table_cell_width = 73
    elif cell_name == "Question":
        table_cell_width = 57
    else:
        table_cell_width = 25
    return table_cell_width


def print_report_to_pdf(pdf, report):
    """ Function which writes the data from report in pdf file."""
    table_cell_height = 6
    pdf.set_font('Times', '', 10)
    column_names = report[0].keys()

    for column in column_names:
        table_cell_width = cell_width(column)
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
            table_cell_width = cell_width(column)
            pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)


class Reasoning:
    def __init__(self):
        self.people = ["Josh", "Thomas", "Ben", "Jack", "Greg", "Sam", "Lily", "Rachel", "Anna", "Jasmine", "Adrian",
                       "Dennis", "Omar", "Max", "Kyle", "Elsa", "Ashly", "Tara", "Erika", "Bianca"]
        self.adverbs = ['is not as', 'is']
        self.phrase = ""
        self.question = ""
        self.person_1 = ""
        self.person_2 = ""
        self.adverb = ""
        self.adjective = ""
        self.user_answer = ""
        self.answer = ""
        self.questions = 0
        self.situation = 0
        self.score = 0
        self.report = []
        with open('resources/adjectives.json') as adjectives_file:
            self.adjectives = load(adjectives_file)

    def get_phrase(self):
        """ Generate a phrase where 2 random persons selected from a list are compared using an adjective."""
        self.person_1, self.person_2 = sample(self.people, 2)
        self.adjective = choice(self.adjectives)
        self.adverb = choice(self.adverbs)

        if self.adverb == 'is':
            self.phrase = f"{self.person_1} {self.adverb} {self.adjective['comparative']} than {self.person_2}."
        elif self.adverb == 'is not as':
            self.phrase = f"{self.person_1} {self.adverb} {self.adjective['adjective']} as {self.person_2}."

    def get_question(self):
        """ Generate a question based on a previous statement."""
        self.questions += 1
        self.situation = randint(0, 1)
        if self.situation == 0:
            self.question = f"Who is {self.adjective['antonym']}?"
        elif self.situation == 1:
            self.question = f"Who is {self.adjective['comparative']}?"

    def find_answer(self):
        """ Find the answer of the question."""
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
        """ Check if user has guessed the correct answer. It adds the exercise to the report."""
        self.user_answer = user_choice
        self.add_report()
        if self.answer == self.user_answer:
            return True
        return False

    def add_report(self):
        """ Insert the phrase, the question, the correct answer and the user's choice
            inside a report list of dictionaries.
        """
        self.report.append({"No": self.questions, "Phrase": self.phrase, "Question": self.question,
                            "Correct answer": self.answer, "User choice": self.user_answer})

    def save_report(self):
        """ Saves the report of this test in a .pdf file. """
        time_now = datetime.now()
        time_format = "%d/%m/%Y %H:%M"
        date_time = time_now.strftime(time_format)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 16)
        pdf.cell(180, 10, 'REASONING TEST REPORT', 0, 1, 'C')
        pdf.cell(180, 10, date_time, 0, 1, 'C')
        pdf.cell(180, 10, f"Score: {self.score}/{self.questions}", 0, 1, 'C')
        pdf.ln(10)

        print_report_to_pdf(pdf, self.report)

        time_format = "%H-%M_%d-%m-%Y"
        date_time = time_now.strftime(time_format)
        pdf.output(f'reports/{date_time}_reasoning_report.pdf', 'F')
        self.report.clear()
