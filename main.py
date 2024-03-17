import os
from prompt_toolkit.layout import D
from prompt_toolkit import HTML, prompt
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.widgets import RadioList, Dialog, Label, Button, Box
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

from scoring import raw_score_table, score_mapping_table, plot_score, second_order_score


class CattellTestApplication:
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        self.current_question = 0
        self.total_questions = 187
        self.answers = [0 for _ in range(self.total_questions)]
        # self.questions = [f'Question {i + 1}' for i in range(self.total_questions)]  # Add your 187 questions here
        self.key_bindings = KeyBindings()
        self.key_bindings.add("tab")(focus_next)
        self.key_bindings.add("s-tab")(focus_previous)

        self.radio_list = RadioList(values=[(1, "Yes"), (2, "between these two"), (3, "No")])
        self.question_radio_list = RadioList(values=[(0, "dummy question")])
        self.navigation_options = [Button(text="Questions", handler=self.question_status),
                                   Button(text="Save", handler=self.save),
                                   Button(text="Load", handler=self.load),
                                   Button(text="Report", handler=self.report)]
        self.question_option = Box(
            body=VSplit(
                [
                    Button(text="Prev", handler=self.prev_question),
                    Button(text="Next", handler=self.next_question)
                ],
                padding=1
            ),
            height=D(min=1, max=3, preferred=3)
        )

        self.question_dialog = Dialog(
            title=f"Question {self.current_question + 1}/{self.total_questions}",
            body=HSplit(
                [
                    Label(text="Which one do you prefer?", dont_extend_height=True),
                    self.radio_list,
                    self.question_option
                ],
                padding=1,
            ),
            buttons=self.navigation_options,
            with_background=True,
        )

        self.status_dialog = Dialog(
            title=f"Questions Status",
            body=HSplit([
                Label(text="Choose the question", dont_extend_height=True),
                self.question_radio_list,
            ],
                padding=1,
            ),
            buttons=[Button(text="Select", handler=self.select_question), *self.navigation_options],
            with_background=True,
        )

        @self.key_bindings.add('q')
        def _(event):
            self.application.exit()

        self.application = Application(
            layout=Layout(HSplit([self.question_dialog])),
            key_bindings=self.key_bindings,
            mouse_support=True,
            full_screen=True,
        )

        self.update_question()

    def save(self):
        self.answers[self.current_question] = self.radio_list.current_value
        with open(f"./data/{self.name}.txt", 'w') as file:
            for item in self.answers:
                file.write(f"{item}\n")

    def load(self):
        with open(f"./data/{self.name}.txt", 'r') as file:
            self.answers = [int(line.strip()) for line in file]
        self.question_status()

    def update_questions_status_radio_list(self):
        radio_list_values = []
        for i in range(self.total_questions):
            status = "<seagreen>Answered</seagreen>" if self.answers[i] != 0 else "<ansired>Not Answered</ansired>"
            radio_list_values.append((i, HTML(f"Question {i + 1}: {status}")))
        self.question_radio_list = RadioList(values=radio_list_values)

    def question_status(self):
        self.answers[self.current_question] = self.radio_list.current_value
        self.update_questions_status_radio_list()
        self.status_dialog.body = HSplit(
            [Label(text="Choose your question:", dont_extend_height=True), self.question_radio_list], padding=1)
        self.application.layout = Layout(HSplit([self.status_dialog]))

    def select_question(self):
        self.current_question = self.question_radio_list.current_value
        self.application.layout = Layout(HSplit([self.question_dialog]))
        self.update_question()

    def update_question(self):
        self.radio_list.current_value = self.answers[self.current_question]
        self.question_dialog.title = f"Question {self.current_question + 1}/{self.total_questions}"

    def next_question(self):
        self.answers[self.current_question] = self.radio_list.current_value
        if self.current_question < self.total_questions - 1:
            self.current_question += 1
            self.update_question()
            # self.application.run()

    def prev_question(self):
        self.answers[self.current_question] = self.radio_list.current_value
        if self.current_question > 0:
            self.current_question -= 1
            self.update_question()
            # self.application.run()

    def run(self):
        self.application.run()

    def report(self):
        raw_score = {}
        for key, questions in raw_score_table.items():
            score = 0
            if key != 'B':
                for q_index in questions[0]:
                    score += self.answers[q_index - 1] - 1
                for q_index in questions[2]:
                    score += 3 - self.answers[q_index - 1]
            else:
                for i in range(3):
                    for q_index in questions[i]:
                        score += 1 if self.answers[q_index - 1] == i + 1 else 0
            raw_score[key] = score

        final_score = {}
        for key, mapping in score_mapping_table.items():
            for i in range(10):
                if mapping[i][0] <= raw_score[key] <= mapping[i][1]:
                    final_score[key] = i + 1

        plot_score(final_score, f"{self.name}'s First Order Factors")
        second_order_scores = second_order_score(final_score, self.sex)
        plot_score(second_order_scores, f"{self.name}'s Second Order Factors")


if __name__ == '__main__':
    print("Welcome to the Cattell's personality test!\n")
    user_name = prompt("Please enter your name: ")
    # Get user's sex using a radio list
    user_sex = radiolist_dialog(
        title="User Sex",
        text="Please select your sex:",
        values=[
            (1, "Male"),
            (2, "Female")
        ]).run()

    # Check if user closed the dialog or did not select an option
    if user_sex is None:
        print("No selection made. Exiting.")
        exit(0)

    if not os.path.exists("./data"):
        os.makedirs("./data")
    if not os.path.exists("./report"):
        os.makedirs("./report")

    app = CattellTestApplication(name=user_name, sex=user_sex)
    app.run()
    print(app.answers)
