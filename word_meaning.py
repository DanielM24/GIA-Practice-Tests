from random import choice, shuffle
from datetime import datetime
from json import load
from fpdf import FPDF


def print_report_to_pdf(pdf, report):
    """ Function which writes the data from report in pdf file."""
    table_cell_width = 30
    table_cell_height = 6
    pdf.set_font('Times', '', 10)
    column_names = report[0].keys()

    for column in column_names:
        if column == 'Words':
            table_cell_width = 70
        else:
            table_cell_width = 30
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
            if column == 'Words':
                table_cell_width = 70
            else:
                table_cell_width = 30
            pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)


class WordMeaning:
    def __init__(self):
        self.report = []
        self.questions = 0
        self.pair = {}
        self.answer = ''
        self.user_answer = 0
        self.score = 0
        with open('resources/words.json') as words_file:
            self.words = load(words_file)

    def get_words(self):
        """ Appends a pair of two words which are linked and generates a random word of the same type. """
        self.pair = choice(self.words)
        possible_word = [[word['word_1'], word['word_2']] for word in self.words
                         if word['type'] == self.pair['type'] and word['word_1'] != self.pair['word_1']]
        self.answer = choice(choice(possible_word))
        self.pair = [self.pair['word_1'], self.answer, self.pair['word_2']]
        shuffle(self.pair)
        self.questions += 1

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
        self.report.append({"Question No": self.questions, "Words": self.pair,
                            "Correct answer": self.answer, "User choice": self.user_answer})

    def save_report(self):
        """ Saves the report of this test in a .pdf file. """
        time_now = datetime.now()
        time_format = "%d/%m/%Y %H:%M"
        date_time = time_now.strftime(time_format)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 16)
        pdf.cell(200, 10, 'WORD MEANING TEST REPORT', 0, 1, 'C')
        pdf.cell(200, 10, date_time, 0, 1, 'C')
        pdf.cell(200, 10, f"Score: {self.score}/{self.questions - 1}", 0, 1, 'C')
        pdf.ln(10)

        print_report_to_pdf(pdf, self.report)

        time_format = "%H-%M_%d-%m-%Y"
        date_time = time_now.strftime(time_format)
        pdf.output(f'reports/{date_time}_word_meaning_report.pdf', 'F')
        self.report.clear()
