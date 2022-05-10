from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

import sqlite3
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

    extended_questions = []

    selected_smiley = None

    def checked(self,instance):
        self.add_extended_questions()
        self.selected_smiley = instance
        print(instance)
        self.ids["submit"].pos_hint = {"x": 0.425}



    def add_extended_questions(self):


        spacing = ((0.2, 0.4), (0.6, 0.4), (0.2, 0.2), (0.6, 0.2))

        if self.selected_smiley == None:
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

class ChangeQuestion(FloatLayout):

    def __init__(self, **kwargs):
        super(ChangeQuestion, self).__init__(**kwargs)

        self.popupWindow = Popup(title="Popup Window", content=self, size_hint=(1, 1))

        self.save_btn = Button(text="save", background_color=(0, 0, 1, 1), size_hint=(0.3, 0.06), pos_hint = {"x": 0.35, "top": 0.1})
        self.save_btn.bind(on_release=self.save)
        self.add_widget(self.save_btn)

        self.close_btn = Button(text="close", background_color=(0, 0, 1, 1), size_hint=(0.1, 0.1), pos_hint = {"x": 0.1, "top": 0.1})
        self.close_btn.bind(on_release=self.close)
        self.add_widget(self.close_btn)
        self.questions = []

    def save(self, instance):

        for i in range(len(self.questions)):
            print(i)
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


class ResponseeTwo(App):
    Window.clearcolor = (1, 1, 1, 1)

    def build(self):
        r = NewResponsee()
        return r


app = ResponseeTwo()
myresponsee = app.build()
question_terminal = ChangeQuestion()
if __name__ == "__main__":
    app.run()