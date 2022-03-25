from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from reasoning import Reasoning
from perceptual_speed import PerceptualSpeed
from number_speed import NumberSpeedAccuracy
from spatial_visualisation import SpatialVisualisation

import numpy as np
import PIL

# ---------------------------- COLORS ------------------------------- #
CHAMPAGNE_PINK = "#F2DFD7"
GHOST_WHITE = "#FEF9FF"
THISTLE = "#D4C1EC"
MAXIMUM_BLUE_PURPLE = "#9F9FED"
MEDIUM_SLATE_BLUE = "#736CED"

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Georgia"
TIMER = None
timer_label = None
GAME_WINDOW = None
exercise = 0
image_pairs = None
buttons = []


# ---------------------------- GAME INFO ------------------------------- #
def show_score():
    if exercise == 1:
        message = f"""    Your final score is: {reasoning.score} / {reasoning.questions}.

    Do you want to download a report for the ‘REASONING’ test?
        """
    elif exercise == 2:
        message = f"""    Your final score is: {perceptual_speed.score} / {perceptual_speed.questions - 1}.

    Do you want to download a report for the ‘PERCEPTUAL SPEED’ test?
        """
    elif exercise == 3:
        message = f"""    Your final score is: {number_speed.score} / {number_speed.questions - 1}.
    
    Do you want to download a report for the ‘NUMBER, SPEED & ACCURACY’ test?
        """
    else:
        message = f"""    Your final score is: {spatial_visualisation.score} / {spatial_visualisation.questions - 1}.
    
    Do you want to download a report for the ‘SPATIAL VISUALISATION’ test?
        """
    buttons_enable(buttons)
    GAME_WINDOW.destroy()

    if messagebox.askyesno(title="End of the test", message=message):
        if exercise == 1:
            reasoning.save_report()
        elif exercise == 2:
            perceptual_speed.save_report()
        elif exercise == 3:
            number_speed.save_report()
        else:
            spatial_visualisation.save_report()
    else:
        pass


# ---------------------------- TIMER ------------------------------- #
def countdown_timer(count):
    global TIMER
    minutes = str(count // 60).rjust(2, '0')
    seconds = str(count % 60).rjust(2, '0')
    timer_label.config(text=f"TIME: {minutes}:{seconds}")
    if count > 0:
        TIMER = GAME_WINDOW.after(1000, countdown_timer, count - 1)
    else:
        show_score()


# ---------------------------- BUTTONS ------------------------------- #
def buttons_disable(menu_buttons):
    for button in menu_buttons:
        button.config(state=DISABLED)


def buttons_enable(menu_buttons):
    for button in menu_buttons:
        button.config(state=NORMAL)
    GAME_WINDOW.destroy()


# ---------------------------- REASONING ------------------------------- #
reasoning = Reasoning()


def check_option_r(question_label: Label, option_1: Button, option_2: Button, user_choice):
    """ Check if the user has selected the correct answer."""
    question_label.destroy()
    option_1.destroy()
    option_2.destroy()
    if reasoning.check_answer(user_choice):
        reasoning.score += 1
        # print(reasoning.score)
    show_phase()


def show_question(phrase_label: Label, question_button: Button):
    reasoning.get_question()
    reasoning.find_answer()

    phrase_label.destroy()
    question_button.destroy()

    question_label = Label(GAME_WINDOW, text=reasoning.question, bg=GHOST_WHITE)
    question_label.config(fg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 20, "bold"), pady=20, padx=100)
    question_label.grid(row=1, column=0, columnspan=2)

    option_1 = Button(GAME_WINDOW, text=reasoning.person_1, highlightthickness=0)
    option_1.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 16, "bold"), relief=GROOVE,
                    command=lambda: check_option_r(question_label, option_1, option_2, reasoning.person_1))
    option_1.grid(row=2, column=0, pady=10, padx=50, sticky="ew")

    option_2 = Button(GAME_WINDOW, text=reasoning.person_2, highlightthickness=0)
    option_2.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 16, "bold"), relief=GROOVE,
                    command=lambda: check_option_r(question_label, option_1, option_2, reasoning.person_2))
    option_2.grid(row=2, column=1, pady=10, padx=50, sticky="ew")

    GAME_WINDOW.protocol("WM_DELETE_WINDOW", lambda: buttons_enable(menu_buttons=buttons))


def show_phase():
    reasoning.get_phrase()

    phrase_label = Label(GAME_WINDOW, text=reasoning.phrase, bg=GHOST_WHITE)
    phrase_label.config(fg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 20, "bold"), pady=20, padx=60)
    phrase_label.grid(row=1, column=0, columnspan=2)

    question_button = Button(GAME_WINDOW, text="CLICK THE SCREEN WHEN READY", highlightthickness=0)
    question_button.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 16, "bold"), relief=GROOVE,
                           command=lambda: show_question(phrase_label, question_button))
    question_button.grid(row=2, column=0, columnspan=2, pady=20, padx=60, sticky="ew")

    GAME_WINDOW.protocol("WM_DELETE_WINDOW", lambda: buttons_enable(menu_buttons=buttons))


def reasoning_game():
    global GAME_WINDOW, timer_label, exercise
    exercise = 1
    reasoning.score = 0
    reasoning.questions = 0
    info_message = """    Each question is about comparing two people.
    You can study this statement for as long as you need to understand it fully.
    When you are ready you must click the mouse. When you have done this the statement will disappear and a question about the statement will be shown together with two possible answers.
    You must now move the mouse pointer to the box which contains the correct answer. When you have done this, the next question will appear and so on until the end of the test.

    The REASONING test runs for about 3 minutes. """
    messagebox.showinfo(title="The ‘REASONING’ test", message=info_message)
    buttons_disable(buttons)

    GAME_WINDOW = Toplevel(main_menu)
    GAME_WINDOW.title("Reasoning")
    GAME_WINDOW.config(padx=50, pady=40, bg=GHOST_WHITE)
    GAME_WINDOW.iconbitmap("resources/my_icon.ico")

    timer_label = Label(GAME_WINDOW, text="TIME: 00:00", bg=GHOST_WHITE)
    timer_label.config(fg=THISTLE, font=(FONT_NAME, 10, "bold"), anchor="ne")
    timer_label.grid(row=0, column=1)

    show_phase()
    countdown_timer(3 * 60)


# ---------------------------- PERCEPTUAL SPEED ------------------------------- #
perceptual_speed = PerceptualSpeed()


def check_option_ps(letters_label: Label, user_choice):
    """ Check if the user has selected the correct answer."""
    if perceptual_speed.check_answer(user_choice):
        perceptual_speed.score += 1
    # print(perceptual_speed.score)
    show_letters(letters_label)


def show_letters(letters_label: Label):
    perceptual_speed.get_letters()
    perceptual_speed.find_answer()
    letters = f"{perceptual_speed.upper_row[0]}   {perceptual_speed.upper_row[1]}   {perceptual_speed.upper_row[2]}" \
              f"   {perceptual_speed.upper_row[3]}\n{perceptual_speed.lower_row[0]}   {perceptual_speed.lower_row[1]}" \
              f"   {perceptual_speed.lower_row[2]}   {perceptual_speed.lower_row[3]}"
    letters_label.config(text=letters)

    GAME_WINDOW.protocol("WM_DELETE_WINDOW", lambda: buttons_enable(menu_buttons=buttons))


def perceptual_speed_game():
    global GAME_WINDOW, timer_label, exercise
    exercise = 2
    perceptual_speed.score = 0
    perceptual_speed.questions = 0
    info_message = """    In this test, you will see four pairs of letters. Each pair has been put into its own box.
    You must decide how many pairs contain letters that are the same.

    The PERCEPTUAL SPEED test runs for about 4 minutes. """

    messagebox.showinfo(title="The ‘PERCEPTUAL SPEED’ test", message=info_message)
    buttons_disable(buttons)

    GAME_WINDOW = Toplevel(main_menu)
    GAME_WINDOW.title("Perceptual Speed")
    GAME_WINDOW.config(padx=40, pady=20, bg=GHOST_WHITE)
    GAME_WINDOW.iconbitmap("resources/my_icon.ico")

    letters_label = Label(GAME_WINDOW, text="", bg=GHOST_WHITE)
    letters_label.config(fg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 40, "bold"), pady=20, padx=100)
    letters_label.grid(row=1, column=0, columnspan=5)

    option_0 = Button(GAME_WINDOW, text="0", highlightthickness=0)
    option_0.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 16, "bold"), relief=GROOVE,
                    command=lambda: check_option_ps(letters_label, 0))
    option_0.grid(row=2, column=0, pady=20, padx=10, sticky="ew")

    option_1 = Button(GAME_WINDOW, text="1", highlightthickness=0)
    option_1.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 16, "bold"), relief=GROOVE,
                    command=lambda: check_option_ps(letters_label, 1))
    option_1.grid(row=2, column=1, pady=20, padx=10, sticky="ew")

    option_2 = Button(GAME_WINDOW, text="2", highlightthickness=0)
    option_2.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 16, "bold"), relief=GROOVE,
                    command=lambda: check_option_ps(letters_label, 2))
    option_2.grid(row=2, column=2, pady=20, padx=10, sticky="ew")

    option_3 = Button(GAME_WINDOW, text="3", highlightthickness=0)
    option_3.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 16, "bold"), relief=GROOVE,
                    command=lambda: check_option_ps(letters_label, 3))
    option_3.grid(row=2, column=3, pady=20, padx=10, sticky="ew")

    option_4 = Button(GAME_WINDOW, text="4", highlightthickness=0)
    option_4.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 16, "bold"), relief=GROOVE,
                    command=lambda: check_option_ps(letters_label, 4))
    option_4.grid(row=2, column=4, pady=20, padx=10, sticky="ew")

    timer_label = Label(GAME_WINDOW, text="TIME: 00:00", bg=GHOST_WHITE)
    timer_label.config(fg=THISTLE, font=(FONT_NAME, 10, "bold"), anchor="ne")
    timer_label.grid(row=0, column=5)

    show_letters(letters_label)
    countdown_timer(4 * 60)


# ---------------------------- NUMBER SPEED & ACCURACY ------------------------------- #
number_speed = NumberSpeedAccuracy()


def check_option_nsp(option_0: Button, option_1: Button, option_2: Button, user_choice):
    """ Check if the user has selected the correct answer."""
    if number_speed.check_answer(user_choice):
        number_speed.score += 1
    # print(number_speed.score)
    show_numbers(option_0, option_1, option_2)


def show_numbers(option_0: Button, option_1: Button, option_2: Button):
    number_speed.get_numbers()
    number_speed.find_answer()

    option_0.config(text=f"{number_speed.numbers[0]}")
    option_1.config(text=f"{number_speed.numbers[1]}")
    option_2.config(text=f"{number_speed.numbers[2]}")

    GAME_WINDOW.protocol("WM_DELETE_WINDOW", lambda: buttons_enable(menu_buttons=buttons))


def number_speed_game():
    global GAME_WINDOW, timer_label, exercise
    exercise = 3
    number_speed.score = 0
    number_speed.questions = 0
    info_message = """    For each problem presented, start by finding the largest and the smallest of the three numbers displayed.
    Having identified those, decide whether the largest or the smallest is further away from the remaining number.

    The NUMBER SPEED & ACCURACY test runs for about 3 minutes. """

    messagebox.showinfo(title="The ‘NUMBER, SPEED & ACCURACY’ test", message=info_message)
    buttons_disable(buttons)

    GAME_WINDOW = Toplevel(main_menu)
    GAME_WINDOW.title("Number Speed & Accuracy")
    GAME_WINDOW.config(padx=25, pady=20, bg=GHOST_WHITE)
    GAME_WINDOW.iconbitmap("resources/my_icon.ico")

    option_0 = Button(GAME_WINDOW, highlightthickness=0)
    option_0.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 22, "bold"), relief=GROOVE,
                    command=lambda: check_option_nsp(option_0, option_1, option_2, number_speed.numbers[0]))
    option_0.grid(row=1, column=0, pady=20, padx=20, sticky="ew")

    option_1 = Button(GAME_WINDOW, highlightthickness=0)
    option_1.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 22, "bold"), relief=GROOVE,
                    command=lambda: check_option_nsp(option_0, option_1, option_2, number_speed.numbers[1]))
    option_1.grid(row=1, column=1, pady=20, padx=20, sticky="ew")

    option_2 = Button(GAME_WINDOW, highlightthickness=0)
    option_2.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 22, "bold"), relief=GROOVE,
                    command=lambda: check_option_nsp(option_0, option_1, option_2, number_speed.numbers[2]))
    option_2.grid(row=1, column=2, pady=20, padx=20, sticky="ew")

    timer_label = Label(GAME_WINDOW, text="TIME: 00:00", bg=GHOST_WHITE)
    timer_label.config(fg=THISTLE, font=(FONT_NAME, 10, "bold"), anchor="ne")
    timer_label.grid(row=0, column=3)

    show_numbers(option_0, option_1, option_2)
    countdown_timer(3 * 60)


# ---------------------------- SPATIAL VISUALISATION ------------------------------- #
spatial_visualisation = SpatialVisualisation()


def check_option_sv(pairs: list[Label], user_choice):
    """ Check if the user has selected the correct answer."""
    global image_pairs
    if spatial_visualisation.check_answer(user_choice):
        spatial_visualisation.score += 1
    # print(spatial_visualisation.score)
    spatial_visualisation.add_report(image_pairs)
    show_images(pairs)


def draw_image(side, angle):
    """Generates a PIL Image of a drawn R with a given side and angle"""
    letter_font = ImageFont.truetype('verdana.ttf', 80)
    # Create a new PIL image
    image = Image.new(mode="RGB", size=(100, 100), color="white")
    # Draw a black R on the image
    draw = ImageDraw.Draw(image)
    draw.text((20, 1), "R", font=letter_font, fill='black', align='center', stroke_width=1,
              stroke_fill='black')
    # Rotate the image
    image = image.rotate(angle)
    # Flip the image horizontally if needed
    if side == 1:
        image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
    return image


def get_pairs_image(images: list):
    """ Function which generates a picture of both pairs. """
    global image_pairs
    pairs_image_rows = []
    for index in range(2):
        pairs_image_row = np.hstack([images[index], images[index + 2]])
        pairs_image_rows.append(pairs_image_row)
    image_pairs = np.vstack([i for i in pairs_image_rows])
    image_pairs = PIL.Image.fromarray(image_pairs)
    image_pairs = image_pairs.resize((75, 75), resample=0)
    # image_pairs.show()


def show_images(pairs: list[Label]):
    spatial_visualisation.get_pairs()
    images = []
    for pair in spatial_visualisation.pairs:
        for letter in pair:
            image = draw_image(letter[0], letter[1])
            images.append(image)
    # Create an image with both pairs together
    get_pairs_image(images)

    for index in range(4):
        images[index] = ImageTk.PhotoImage(images[index])
        pairs[index].image = images[index]
        pairs[index].config(image=images[index])

    GAME_WINDOW.protocol("WM_DELETE_WINDOW", lambda: buttons_enable(menu_buttons=buttons))


def spatial_visualisation_game():
    global GAME_WINDOW, timer_label, exercise
    exercise = 4
    spatial_visualisation.score = 0
    spatial_visualisation.questions = 0
    pairs = []
    info_message = """    This test is designed to see how quickly you can turn shapes around in your head.
    The challenge is to see how many boxes contain two shapes that are the same.

    The SPATIAL VISUALISATION test runs for about 3 minutes. """

    messagebox.showinfo(title="The ‘SPATIAL VISUALISATION’ test", message=info_message)
    buttons_disable(buttons)

    GAME_WINDOW = Toplevel(main_menu)
    GAME_WINDOW.title("Spatial Visualisation")
    GAME_WINDOW.config(padx=50, pady=20, bg=GHOST_WHITE)
    GAME_WINDOW.iconbitmap("resources/my_icon.ico")

    pair_1_1 = Label(GAME_WINDOW)
    pair_1_1.grid(row=1, column=1)
    pairs.append(pair_1_1)

    pair_1_2 = Label(GAME_WINDOW)
    pair_1_2.grid(row=2, column=1)
    pairs.append(pair_1_2)

    pair_2_1 = Label(GAME_WINDOW)
    pair_2_1.grid(row=1, column=3)
    pairs.append(pair_2_1)

    pair_2_2 = Label(GAME_WINDOW)
    pair_2_2.grid(row=2, column=3)
    pairs.append(pair_2_2)

    option_0 = Button(GAME_WINDOW, text="0", highlightthickness=0, width=3)
    option_0.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 22, "bold"), relief=GROOVE,
                    command=lambda: check_option_sv(pairs=pairs, user_choice=0))
    option_0.grid(row=3, column=0, pady=25, padx=10, sticky="ew")

    option_1 = Button(GAME_WINDOW, text="1", highlightthickness=0, width=3)
    option_1.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 22, "bold"), relief=GROOVE,
                    command=lambda: check_option_sv(pairs, user_choice=1))
    option_1.grid(row=3, column=2, pady=25, padx=10, sticky="ew")

    option_2 = Button(GAME_WINDOW, text="2", highlightthickness=0, width=3)
    option_2.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 22, "bold"), relief=GROOVE,
                    command=lambda: check_option_sv(pairs, user_choice=2))
    option_2.grid(row=3, column=4, pady=25, sticky="ew")

    timer_label = Label(GAME_WINDOW, text="TIME: 00:00", bg=GHOST_WHITE)
    timer_label.config(fg=THISTLE, font=(FONT_NAME, 10, "bold"), anchor="ne")
    timer_label.grid(row=0, column=5)

    show_images(pairs)
    countdown_timer(3 * 60)


# ---------------------------- MAIN MENU ------------------------------- #
main_menu = Tk()
main_menu.title("GIA Practice Tests")
main_menu.iconbitmap("resources/my_icon.ico")
main_menu.config(padx=75, pady=40, bg=GHOST_WHITE)

header_label = Label(text="THOMAS INTERNATIONAL", bg=GHOST_WHITE)
header_label.config(fg=MAXIMUM_BLUE_PURPLE, font=(FONT_NAME, 15, "bold"), pady=10)
header_label.grid(row=0, column=0, columnspan=5)

title_label = Label(text="GIA PRACTICE TESTS*", bg=GHOST_WHITE)
title_label.config(fg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 25, "bold"))
title_label.grid(row=1, column=0, columnspan=5)

disclaimer_label = Label(text="*(Non-official)", bg=GHOST_WHITE)
disclaimer_label.config(fg=MEDIUM_SLATE_BLUE, font=(FONT_NAME, 10, "italic"))
disclaimer_label.grid(row=2, column=3, columnspan=2, pady=10)

reasoning_game_button = Button(text="REASONING", highlightthickness=0)
reasoning_game_button.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, relief=GROOVE,
                             font=(FONT_NAME, 15, "bold"), command=reasoning_game)
reasoning_game_button.grid(row=3, column=0, columnspan=5, pady=20, padx=50, sticky="ew")
buttons.append(reasoning_game_button)

perceptual_speed_game_button = Button(text="PERCEPTUAL SPEED", highlightthickness=0)
perceptual_speed_game_button.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, relief=GROOVE,
                                    font=(FONT_NAME, 15, "bold"), command=perceptual_speed_game)
perceptual_speed_game_button.grid(row=4, column=0, columnspan=5, pady=10, padx=50, sticky="ew")
buttons.append(perceptual_speed_game_button)

number_speed_game_button = Button(text="NUMBER SPEED & ACCURACY", highlightthickness=0)
number_speed_game_button.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, relief=GROOVE,
                                font=(FONT_NAME, 15, "bold"), command=number_speed_game)
number_speed_game_button.grid(row=5, column=0, columnspan=5, pady=20, padx=50, sticky="ew")
buttons.append(number_speed_game_button)

spatial_visualisation_game_button = Button(text="SPATIAL VISUALISATION", highlightthickness=0)
spatial_visualisation_game_button.config(fg=CHAMPAGNE_PINK, bg=MEDIUM_SLATE_BLUE, relief=GROOVE,
                                         font=(FONT_NAME, 15, "bold"), command=spatial_visualisation_game)
spatial_visualisation_game_button.grid(row=6, column=0, columnspan=5, pady=10, padx=50, sticky="ew")
buttons.append(spatial_visualisation_game_button)

my_logo = PhotoImage(file="resources/my_logo.png")
my_logo_label = Label(main_menu, image=my_logo, bg=GHOST_WHITE)
my_logo_label.grid(row=7, column=1, columnspan=3, sticky="ew")

main_menu.mainloop()
