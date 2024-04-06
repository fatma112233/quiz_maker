from tkinter import messagebox
import openai
from tkinter import *


def make_error(m):
    messagebox.showinfo(title="Error", message=m)


def check_c(c, window, score_label):
    global score, n
    if (f_quiz[n]["a"][0]).lower() == c:
        score += 1
    else:
        messagebox.showinfo(title="Wrong Answer", message=f"Correct answer: {f_quiz[n]["a"]}")
    n += 1
    window.destroy()

    if n < len(f_quiz):
        ui_question(score_label)
    else:
        score_label.config(text=f"Final Score: {score}/{n}")


def ui_question(score_label):
    global n
    q_dict = f_quiz[n]
    q_window = Tk()
    q_window.title(f"Question {n + 1}")
    q_window.config(padx=50, pady=50)

    q_label = Label(q_window, text=f"{q_dict['q']}")
    q_label.grid(row=0, column=0, columnspan=3)

    c1_button = Button(q_window, width=41, text=f"{q_dict['c'][0]}", command=lambda: check_c("a", q_window, score_label))
    c1_button.grid(row=1, column=0)

    c2_button = Button(q_window, width=41, text=f"{q_dict['c'][1]}", command=lambda: check_c("b", q_window, score_label))
    c2_button.grid(row=1, column=1)

    c3_button = Button(q_window, width=41, text=f"{q_dict['c'][2]}", command=lambda: check_c("c", q_window, score_label))
    c3_button.grid(row=1, column=2)


def organize_quiz(q):
    global f_quiz
    for line in q.split("\n"):
        if len(line) != 0:
            line = line.strip()
            if line[0].lower() == "q":
                question = line
                c = []
            elif line[1] == ")":
                c.append(line)
            elif line[0].lower() == "a":
                f_quiz.append({"q": question, "c": c, "a": line[(line.index(")")-1):]})
    ui_question(score_label)


def make_quiz():
    try:
        global score, f_quiz, n
        score = 0
        f_quiz = []
        n = 0

        topic = topic_entry.get()
        material = material_entry.get()

        # put the api key between quotation
        openai.api_key = ""

        # material thing
        n_gpt = num_q_entry.get()
        if n_gpt.isdigit() and int(n_gpt) > 0:
            n_gpt = int(n_gpt)
            if len(material) == 0 and len(topic) > 0:
                print(len(material), len(topic))
                input_wanted = (f"provide a quiz that has {n_gpt} questions, each question starts with 'q'"
                                f"followed by the number of the question where it is only one line in the topic of "
                                f"{topic} make the question a multiple choice one (three choices) where the choices are"
                                f" short and provide the answer after each question")
            elif len(material) > 0 and len(topic) == 0:
                input_wanted = (f"provide a quiz that has {n_gpt} questions, each question starts with 'q'"
                                f"followed by the number of the question where it is only one line using '{material}' "
                                f"make the question a multiple choice one (three choices) where the choices are short"
                                f" and provide the answer after each question")
            else:
                make_error("If have material do not add topic")
            result = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": input_wanted}
                ]
            )

            organize_quiz(result["choices"][0]["message"]["content"])
        else:
            make_error("Please enter a valid positive integer for the number of questions.")
    except Exception as e:
        make_error(f"An error occurred: {e}")


# UI
window = Tk()
window.title("Quiz Maker")
window.config(padx=50, pady=50)

num_q_label = Label(text="number of questions:")
num_q_label.grid(row=0, column=0)

topic_label = Label(text="Topic:")
topic_label.grid(row=1, column=0)

material_label = Label(text="material:")
material_label.grid(row=2, column=0)

num_q_entry = Entry(width=21)
num_q_entry.grid(row=0, column=1)
num_q_entry.focus()

topic_entry = Entry(width=21)
topic_entry.grid(row=1, column=1)

material_entry = Entry(width=21)
material_entry.grid(row=2, column=1)

score_label = Label(window, text="")
score_label.grid(row=3, column=0, columnspan=2)

generate_button = Button(width=41, text="Generate Quiz", command=make_quiz)
generate_button.grid(row=4, column=0, columnspan=2)

window.mainloop()
