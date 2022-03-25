from random import sample, shuffle
from datetime import datetime
from fpdf import FPDF


def print_report_to_pdf(pdf, report):
    """ Function which writes the data from report in pdf file."""
    table_cell_width = 30
    table_cell_height = 6
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
            pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)


class NumberSpeedAccuracy:
    def __init__(self):
        self.numbers = []
        self.report = []
        self.questions = 0
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
        self.numbers = sorted(sample(range(2, 28), 3))
        while self.numbers[2] - self.numbers[0] > 9 \
                or self.numbers[2] - self.numbers[1] < 2 \
                or self.numbers[1] - self.numbers[0] < 2 \
                or self.numbers[2] - self.numbers[1] == self.numbers[1] - self.numbers[0]:
            self.numbers = sorted(sample(range(2, 30), 3))
        shuffle(self.numbers)
        self.questions += 1

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
        self.report.append({"Question No": self.questions, "Numbers": self.numbers,
                            "Correct answer": self.answer, "User choice": self.user_answer})

    def save_report(self):
        """ Saves the report of this test in a .pdf file. """
        time_now = datetime.now()
        time_format = "%d/%m/%Y %H:%M"
        date_time = time_now.strftime(time_format)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 16)
        pdf.cell(200, 10, 'NUMBER, SPEED & ACCURACY TEST REPORT', 0, 1, 'C')
        pdf.cell(200, 10, date_time, 0, 1, 'C')
        pdf.cell(200, 10, f"Score: {self.score}/{self.questions - 1}", 0, 1, 'C')
        pdf.ln(10)

        print_report_to_pdf(pdf, self.report)

        time_format = "%H-%M_%d-%m-%Y"
        date_time = time_now.strftime(time_format)
        pdf.output(f'reports/{date_time}_number_speed_report.pdf', 'F')
