from prompt_toolkit import HTML
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.styles import BaseStyle
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.widgets import RadioList, Dialog, Label, Button, Box
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import D
from prompt_toolkit.layout.controls import FormattedTextControl


class CattellTestApplication:
    def __init__(self):
        self.current_question = 0
        self.total_questions = 187
        self.answers = [0 for _ in range(self.total_questions)]
        # self.questions = [f'Question {i + 1}' for i in range(self.total_questions)]  # Add your 187 questions here
        self.key_bindings = KeyBindings()
        self.key_bindings.add("tab")(focus_next)
        self.key_bindings.add("s-tab")(focus_previous)
        # self.radio_lists = [
        #     RadioList([(1, 'Option A'), (2, 'Option B'), (3, 'Option C')])
        #     for _ in range(self.total_questions)
        # ]
        self.radio_list = RadioList(values=[(1, "Yes"), (2, "between these two"), (3, "No")])
        self.question_radio_list = RadioList(values=[(0, "Question 1")])

        self.question_dialog = Dialog(
            title=f"Question {self.current_question + 1}/{self.total_questions}",
            body=HSplit(
                [Label(text="Which one do you prefer?", dont_extend_height=True), self.radio_list],
                padding=1,
            ),
            buttons=[
                Button(text="Prev", handler=self.prev_question),
                Button(text="Next", handler=self.next_question),
            ],
            with_background=True,
        )

        self.status_dialog = Dialog(
            title=f"Questions Status",
            body=HSplit(
                [Label(text="Choose the question", dont_extend_height=True), self.question_radio_list],
                padding=1,
            ),
            buttons=[
                Button(text="Select", handler=self.select_question),
            ],
            with_background=True,
        )
        self.options = [Button(text="Questions", handler=self.question_status, ), Button(text="Save"),
                        Button(text="Load"), Button(text="Report")]
        self.option_box = Box(body=VSplit(self.options, padding=1), height=D(min=1, max=3, preferred=3))

        # @self.key_bindings.add('enter')
        # def _(event):
        #     self.handle_enter()
        #
        @self.key_bindings.add('right')
        def _(event):
            self.next_question()

        @self.key_bindings.add('left')
        def _(event):
            self.prev_question()

        @self.key_bindings.add('q')
        def _(event):
            self.application.exit()

        @self.key_bindings.add('f')
        def _(event):
            self.application.layout.focus(self.option_box)

        self.application = Application(
            layout=Layout(HSplit([
                self.question_dialog,
                self.option_box,
            ])),
            key_bindings=self.key_bindings,
            mouse_support=True,
            full_screen=True,
        )

        self.update_question()

    def update_questions_status_radio_list(self):
        radio_list_values = []
        for i in range(self.total_questions):
            status = "<seagreen>Answered</seagreen>" if self.answers[i] != 0 else "<ansired>Not Answered</ansired>"
            radio_list_values.append((i, HTML(f"Question {i + 1}: {status}")))
        self.question_radio_list = RadioList(values=radio_list_values)

    def question_status(self):
        self.update_questions_status_radio_list()
        self.status_dialog.body = HSplit(
            [Label(text="Choose your question:", dont_extend_height=True), self.question_radio_list], padding=1)
        self.application.layout = Layout(HSplit([
            self.status_dialog,
            Box(body=VSplit(self.options, padding=1), height=D(min=1, max=3, preferred=3))]))

    def select_question(self):
        self.current_question = self.question_radio_list.current_value
        self.application.layout = Layout(HSplit([
            self.question_dialog,
            Box(body=VSplit(self.options, padding=1), height=D(min=1, max=3, preferred=3))]))
        self.update_question()

    def update_question(self):
        self.radio_list.current_value = self.answers[self.current_question]
        self.question_dialog.title = f"Question {self.current_question + 1}/{self.total_questions}"
        # self.application.layout = Layout(self.dialog)
        # self.application = Application(
        #     layout=Layout(
        #         HSplit([
        #             Window(content=FormattedTextControl(text=self.questions[self.current_question])),
        #             self.radio_lists[self.current_question],
        #         ])
        #     ),
        #     key_bindings=self.key_bindings,
        #     full_screen=True
        # )

    # def handle_enter(self):
    #     self.answers[self.current_question] = self.radio_lists[self.current_question].current_value
    #     print(f"Answer for question {self.current_question + 1}: {self.answers[self.current_question]}")
    #     self.next_question()

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


from prompt_toolkit.shortcuts import button_dialog, radiolist_dialog

if __name__ == '__main__':
    # result = button_dialog(
    #     title='Button dialog example',
    #     text='Do you want to confirm?',
    #     buttons=[
    #         ('Yes', True),
    #         ('No', False),
    #         ('Maybe...', None)
    #     ],
    # ).run()
    # answers = [None for _ in range(total_questions)]
    # for i in range(5):
    #     result = radiolist_dialog(
    #         title=f"Question {i + 1}/{total_questions}",
    #         text="Which one do you prefer?",
    #         values=[
    #             (1, "Yes"),
    #             (2, "Something in between"),
    #             (3, "No")
    #         ]
    #     ).run()
    #     answers.append(result)
    # print(answers)
    app = CattellTestApplication()
    app.run()
    print(app.answers)
