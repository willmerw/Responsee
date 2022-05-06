from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import sqlite3
import matplotlib.pyplot as plt
import numpy as np



class NewResponsee(FloatLayout):
    # lista som representerar antalet tryck på respektive gubbe
    alla_smileys = [0, 0, 0, 0]  # mycket missnojd, missnojd, nojd, mycket nojd

    mycket_missnojd = ObjectProperty(None)
    missnojd = ObjectProperty(None)
    nojd = ObjectProperty(None)
    mycket_nojd = ObjectProperty(None)
    pie_data = ObjectProperty(None)
    min_label = ObjectProperty(None)
    bar_data = ObjectProperty

    # visar att man trycker på en knapp, först byter bild (on click), sen tillbaka till orginal (on release)
    def mycket_missnojd_on(self):
        self.ids.mycket_missnojd_bilden.source = "arg1.png"

    def mycket_missnojd_off(self):
        self.ids.mycket_missnojd_bilden.source = "arg.png"

    def missnojd_on(self):
        self.ids.missnojd_bilden.source = "missnojd1.png"

    def missnojd_off(self):
        self.ids.missnojd_bilden.source = "missnojd.png"

    def nojd_on(self):
        self.ids.nojd_bilden.source = "nojd1.png"

    def nojd_off(self):
        self.ids.nojd_bilden.source = "nojd.png"

    def mycket_nojd_on(self):
        self.ids.mycket_nojd_bilden.source = "mycket nojd1.png"

    def mycket_nojd_off(self):
        self.ids.mycket_nojd_bilden.source = "mycket nojd.png"

        # lägger till 1 för varje tryck

    def knapp_tryck(self, instance):
        if instance == self.mycket_missnojd:
            self.alla_smileys[0] += 1
        elif instance == self.missnojd:
            self.alla_smileys[1] += 1
        elif instance == self.nojd:
            self.alla_smileys[2] += 1
        elif instance == self.mycket_nojd:
            self.alla_smileys[3] += 1

        # kommer tas bort sedan
        print("Mycket Missnöjd:", self.alla_smileys[0])
        print("Missnöjd:", self.alla_smileys[1])
        print("Nöjd:", self.alla_smileys[2])
        print("Mycket nöjd:", self.alla_smileys[3])
        print(self.alla_smileys)
        print(".........................................")

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


class ResponseeTwo(App):
    Window.clearcolor = (1, 1, 1, 1)

    def build(self):
        return NewResponsee()


if __name__ == "__main__":
    ResponseeTwo().run()