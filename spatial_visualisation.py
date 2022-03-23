from random import sample, randint, shuffle
from datetime import datetime
from fpdf import FPDF


def print_report_to_pdf(pdf, report):
    """ Function which writes the data from report in pdf file."""
    table_cell_width = 30
    table_cell_height = 12
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
            if column == "Pairs":
                x_cord = pdf.get_x() + 10
                y_cord = pdf.get_y() + 1
                pdf.image(line[column], w=10, h=10, x=x_cord, y=y_cord)
                pdf.cell(table_cell_width, table_cell_height, " ", align='C', border=1)
            else:
                value = str(line[column])
                pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)


class SpatialVisualisation:
    def __init__(self):
        self.picture_angles = [(0, 0), (0, 90), (0, 180), (0, 270), (1, 0), (1, 90), (1, 180), (1, 270)]
        self.answer = None
        self.user_answer = None
        self.pairs = None
        self.questions = 0
        self.score = 0
        self.report = []

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
        """ Generate pairs of tuples which represents the side and the angle of the picture."""
        self.answer = randint(0, 2)
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
        self.questions += 1

    def check_answer(self, user_choice):
        """ Check if user has guessed the correct answer."""
        self.user_answer = user_choice
        if self.answer == self.user_answer:
            return True
        return False

    def add_report(self, images):
        """ Insert an image of the pairs shown along with the correct answer and the user's choice
            inside a report list.
        """
        self.report.append({"Question No": self.questions, "Pairs": images,
                            "Correct answer": self.answer, "User choice": self.user_answer})

    def save_report(self):
        """ Saves the report of this test in a .pdf file. """
        time_now = datetime.now()
        time_format = "%d/%m/%Y %H:%M"
        date_time = time_now.strftime(time_format)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 16)
        pdf.cell(200, 10, 'SPATIAL VISUALISATION TEST REPORT', 0, 1, 'C')
        pdf.cell(200, 10, date_time, 0, 1, 'C')
        pdf.cell(200, 10, f"Score: {self.score}/{self.questions - 1}", 0, 1, 'C')
        pdf.ln(10)

        print_report_to_pdf(pdf, self.report)

        time_format = "%H-%M_%d-%m-%Y"
        date_time = time_now.strftime(time_format)
        pdf.output(f'reports/{date_time}_spatial_visualisation_report.pdf', 'F')
