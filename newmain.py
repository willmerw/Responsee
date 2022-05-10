from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
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

    selected_smiley = None

    def checked(self):
        self.ids["submit"].pos_hint = {"x": 0.425}
        for i in self.children:
            try:
                if i.group == "questions":
                    i.background_color = (1,1,1,1)
            except AttributeError:
                pass

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

                for i in self.children:
                    try:
                        if i.group == "questions":
                            i.background_color = (1, 1, 1, 0)
                            i.state = "normal"
                    except AttributeError:
                        pass


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
        question_menu()

class ChangeQuestion(FloatLayout):

    def save(self):
        print(self.children)
    pass


def question_menu():
    show = ChangeQuestion()

    popupWindow = Popup(title="Popup Window", content=show, size_hint=(1,1))



    popupWindow.open()

class ResponseeTwo(App):
    Window.clearcolor = (1, 1, 1, 1)

    def build(self):
        r = NewResponsee()
        return r

app = ResponseeTwo

if __name__ == "__main__":
    ResponseeTwo().run()