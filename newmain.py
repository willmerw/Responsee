from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
import numpy as np


class NewResponsee(FloatLayout):

    # lista som representerar antalet tryck på respektive gubbe
    alla_smileys = [0, 0, 0, 0]  # (mycket missnojd, missnojd, nojd, mycket nojd)

    mycket_missnojd = ObjectProperty(None)
    missnojd = ObjectProperty(None)
    nojd = ObjectProperty(None)
    mycket_nojd = ObjectProperty(None)
    pie_data = ObjectProperty(None)
    min_label = ObjectProperty(None)
    bar_data = ObjectProperty(None)
    submit = ObjectProperty(None)

    smiley_list = ["mycket_missnojd", "missnojd", "nojd", "mycket_nojd"]

    questions = ["Volym", "För svårt", "Inte roligt", "Något annat"]
    question_counter = []
    unique_questions = []

    main_questions = "Hur var lektionen idag?"
    extended_questions = []

    selected_smiley = None

    def __init__(self, **kwargs):
        super(NewResponsee, self).__init__(**kwargs)

        self.main_question = Label(text=self.main_questions, font_size=50, color="black", pos_hint={"y": 0.3})
        self.add_widget(self.main_question)

    def checked(self, instance):
        self.add_extended_questions()
        self.selected_smiley = instance
        self.ids["submit"].pos_hint = {"x": 0.425}

    def add_extended_questions(self):

        spacing = ((0.2, 0.4), (0.6, 0.4), (0.2, 0.2), (0.6, 0.2))

        if not self.selected_smiley:
            for i in range(len(self.questions)):

                a = ToggleButton(pos_hint={"x": spacing[i][0], "top": spacing[i][1]}, size_hint=(0.2, 0.05),background_color = (1,1,1,1), group = "questions", text=self.questions[i])
                self.extended_questions.append(a)
                self.add_widget(a)

    def submit_button(self):

        for i in self.smiley_list:
            if self.ids[i].state == "down":

                self.selected_smiley = self.ids[i]

                if self.selected_smiley == self.mycket_missnojd:
                    self.alla_smileys[0] += 1
                elif self.selected_smiley == self.missnojd:
                    self.alla_smileys[1] += 1
                elif self.selected_smiley == self.nojd:
                    self.alla_smileys[2] += 1
                elif self.selected_smiley == self.mycket_nojd:
                    self.alla_smileys[3] += 1

                self.ids[i].state = "normal"

                self.ids["submit"].pos_hint = {"x": 1}

                for question in self.extended_questions:
                    self.remove_widget(question)

                self.selected_smiley = None
        for i in self.extended_questions:
            if i.state == "down":
                if i.text not in self.unique_questions:
                    self.unique_questions.append(i.text)
                self.question_counter.append(i.text)

    def stat_button(self, instance):
        if instance == self.bar_data:
            plt.style.use("fivethirtyeight")
            w = 0.2
            data_skala = ['Mycket missnöjd', 'Missnöjd', 'Nöjd', 'Mycket nöjd']  # skalan som visas
            bar1 = np.arange(len(data_skala))
            farg_lista = ("red", "orange", "#1E90FF", "#00FA9A")
            plt.bar(bar1, self.alla_smileys, w, color=farg_lista, edgecolor='black')
            plt.xticks(bar1, data_skala)
            plt.xlabel("Antal tryck")
            plt.ylabel("Antal elever")
            plt.legend()
            plt.show()

        if instance == self.pie_data:
            plt.style.use("fivethirtyeight")
            data_skala = ['Mycket missnöjd', 'Missnöjd', 'Nöjd', 'Mycket nöjd']  # skalan som visas
            explode = (0.1, 0, 0, 0)  # dra ut en slice ur pie
            colors = ["red", "orange", "#1E90FF", "#00FA9A"]

            plt.pie(self.alla_smileys, explode=explode, labels=data_skala, colors=colors, autopct="%1.1f%%",
                    startangle=90, wedgeprops={"edgecolor": "black"})

            plt.axis('equal')
            plt.tight_layout()
            plt.legend()
            plt.show()

    def open_questions(self):
        question_terminal.open()

    def open_questionstats(self):
        question_stats.open()


class ChangeQuestion(FloatLayout):

    def __init__(self, **kwargs):
        super(ChangeQuestion, self).__init__(**kwargs)

        self.popupWindow = Popup(title="Popup Window", content=self, size_hint=(1, 1))

        self.save_btn = Button(text="save", background_color=(0, 0, 1, 1), size_hint=(0.3, 0.06), pos_hint={"x": 0.35, "top": 0.1})
        self.save_btn.bind(on_release=self.save)
        self.add_widget(self.save_btn)

        self.close_btn = Button(text="close", background_color=(0, 0, 1, 1), size_hint=(0.1, 0.1), pos_hint={"x": 0.1, "top": 0.1})
        self.close_btn.bind(on_release=self.close)
        self.add_widget(self.close_btn)
        self.questions = []

        self.title = TextInput(text=myresponsee.main_questions, size_hint = (0.3, 0.06), pos_hint={"x": 0.35, "top": 0.8})
        self.add_widget(self.title)

    def save(self, instance):

        for i in range(len(self.questions)):
            myresponsee.questions[i] = self.questions[i].text

    def open(self):

        for i in range(len(myresponsee.questions)):
            spacing = 0.1 + (0.1 * i)
            a = TextInput(pos_hint={"x": 0.35, "top": 0.3 + spacing}, size_hint=(0.3, 0.06),
                          text=myresponsee.questions[i])
            self.questions.append(a)
            self.add_widget(a)

        self.popupWindow.open()

    def close(self, instance):
        self.popupWindow.dismiss()
        self.questions = []


class QuestionStats(FloatLayout):

    def __init__(self, **kwargs):
        super(QuestionStats, self).__init__(**kwargs)

        self.popupWindow = Popup(title="Popup Window", content=self, size_hint=(0.4, 0.7))

        self.close_btn = Button(text="close", background_color=(0, 0, 1, 1), size_hint=(0.1, 0.1), pos_hint = {"x": 0.1, "top": 0.1})
        self.close_btn.bind(on_release=self.close)
        self.add_widget(self.close_btn)
        self.questions = []

    def open(self):
        for i in range(len(myresponsee.unique_questions)):
            spacing = 0.1 + (0.1 * i)
            a = Label(pos_hint={"x": 0.35, "top": 1 - spacing}, size_hint=(0.3, 0.06), text=myresponsee.unique_questions[i],)
            count = Label(pos_hint={"x": 0.55, "top": 1 - spacing}, size_hint=(0.3, 0.06), text=str(myresponsee.question_counter.count(myresponsee.unique_questions[i])))
            print(myresponsee.question_counter.count(myresponsee.unique_questions[i]))
            self.questions.append(a)
            self.questions.append(count)
            self.add_widget(a)
            self.add_widget(count)

        self.popupWindow.open()

    def close(self, instance):
        self.popupWindow.dismiss()
        for i in self.questions:
            self.remove_widget(i)
        self.questions = []


class ResponseeTwo(App):
    Window.clearcolor = (1, 1, 1, 1)

    def build(self):
        r = NewResponsee()
        return r


app = ResponseeTwo()
myresponsee = app.build()
question_terminal = ChangeQuestion()
question_stats = QuestionStats()
if __name__ == "__main__":
    app.run()
