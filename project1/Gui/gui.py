import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame
from tkmacosx import Button

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Algorithm.beale_function import bale_function
from Algorithm.genetic_algorithm import GeneticAlgorithm
from Helpers.enums import SelectionType, MutationType, CrossingType

LEFT_FRAME_BACKGROUND_COLOR = "#FFFFFF"
RIGHT_FRAME_BACKGROUND_COLOR = "#E5E5E5"
RIGHT_FRAME_TITLE_COLOR = "#104FAF"
RIGHT_FRAME_FONT_COLOR = "#1872FB"


class MainApplication(tk.Frame):
    right_scrollable_frame: Frame

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.box = tk.Entry(master)
        self.width = self.master.winfo_screenwidth() / 1.45
        self.height = self.master.winfo_screenheight() / 1.25
        self.max_min_method = tk.IntVar()
        self.method = tk.IntVar()
        self.configure_gui()
        self.create_frames()

    def configure_gui(self):
        self.master.title("OE - Projekt nr 1")
        self.master.geometry("%ix%i" % (self.width, self.height))
        self.master.configure(bg=LEFT_FRAME_BACKGROUND_COLOR)
        # self.master.resizable(0, 0)

    def create_frames(self):
        self.left_frame = tk.Frame(width=self.width * 0.50, height=self.height - 20,
                                   background=LEFT_FRAME_BACKGROUND_COLOR)
        self.left_frame.grid(row=0, column=0)
        self.set_canvas_to_left_frame()

        self.right_frame = tk.Frame(width=self.width * 0.50, height=self.height - 20,
                                    background=RIGHT_FRAME_BACKGROUND_COLOR)
        self.right_frame.grid(row=0, column=1)
        self.set_canvas_to_right_frame()

    def set_canvas_to_left_frame(self):
        left_canvas = tk.Canvas(self.left_frame, width=self.width * 0.50, height=self.height - 20,
                                highlightthickness=0,
                                background="white")

        left_scrollbar = tk.Scrollbar(self.left_frame, orient="vertical", command=left_canvas.yview)
        self.left_scrollable_frame = tk.Frame(left_canvas)

        self.left_scrollable_frame.bind(
            "<Configure>",
            lambda e: left_canvas.configure(
                scrollregion=left_canvas.bbox("all")
            )
        )
        left_canvas.create_window((0, 0), window=self.left_scrollable_frame, anchor=tk.N + tk.W)
        left_canvas.configure(yscrollcommand=left_scrollbar.set)

        left_canvas.pack(side="left", fill="y", expand=False, pady=10)
        left_scrollbar.pack(side="right", fill="y", pady=10)

    def set_canvas_to_right_frame(self):
        right_canvas = tk.Canvas(self.right_frame, width=self.width * 0.50 - 30, height=self.height - 20,
                                 highlightthickness=0,
                                 background=RIGHT_FRAME_BACKGROUND_COLOR)

        right_scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=right_canvas.yview,
                                       bg=RIGHT_FRAME_BACKGROUND_COLOR)
        self.right_scrollable_frame = tk.Frame(right_canvas, background=RIGHT_FRAME_BACKGROUND_COLOR)

        self.right_scrollable_frame.bind(
            "<Configure>",
            lambda e: right_canvas.configure(
                scrollregion=right_canvas.bbox("all")
            )
        )

        self.create_right_frame_widgets()

        right_canvas.create_window((0, 0), window=self.right_scrollable_frame, anchor=tk.N + tk.W)
        right_canvas.configure(yscrollcommand=right_scrollbar.set)

        right_canvas.pack(side="left", fill="y", expand=False, pady=10)
        right_scrollbar.pack(side="right", fill="y", pady=10)

    def create_right_frame_widgets(self):
        self.set_lables_right_frame()
        self.create_radio_button("Maksymalizacja", 1, self.max_min_method, 1, 1, "W")
        self.create_radio_button("Minimalizacja", 2, self.max_min_method, 1, 1, "E")

        self.x1_from_range = self.create_spinbox(-100, 100, 1, 11, "normal")
        self.x1_from_range.grid(row=2, column=0, padx=(0, 112), sticky="E")

        x1_to_range = self.create_spinbox(-100, 100, 1, 11, "normal")
        x1_to_range.grid(row=2, column=0, padx=(0, 10), sticky="E")

        x2_from_range = self.create_spinbox(-100, 100, 1, 11, "normal")
        x2_from_range.grid(row=3, column=0, padx=(0, 112), sticky="E")

        x2_to_range = self.create_spinbox(-100, 100, 1, 11, "normal")
        x2_to_range.grid(row=3, column=0, padx=(0, 10), sticky="E")

        self.chromosome_precision = self.create_spinbox(0, 1, 0.01, 28, "normal")
        self.chromosome_precision.grid(row=5, column=0, padx=(0, 10), sticky="E")

        self.population_size = self.create_spinbox(0, 1000, 1, 28, "normal")
        self.population_size.grid(row=6, column=0, padx=(0, 10), sticky="E")

        self.num_of_epoch = self.create_spinbox(0, 1000, 1, 28, "normal")
        self.num_of_epoch.grid(row=7, column=0, padx=(0, 10), sticky="E")

        self.selection_option = ttk.Combobox(self.right_scrollable_frame,
                                             values=("Selekcja najlepszych", "Koło ruletki", "Selekcja turniejowa"),
                                             width=20)
        self.selection_option.set("-- Nie wybrano --")
        self.selection_option.bind("<<ComboboxSelected>>", self.justamethod)
        self.selection_option.grid(row=8, column=0, padx=(0, 18), sticky="E")

        self.crossing_option = ttk.Combobox(self.right_scrollable_frame,
                                            values=("Jednopunktowe", "Dwupunktowe",
                                                    "Trzypunktowe", "Jednorodne"),
                                            width=20)
        self.crossing_option.set("-- Nie wybrano --")
        self.crossing_option.bind("<<ComboboxSelected>>", self.justamethod)
        self.crossing_option.grid(row=9, column=0, padx=(0, 18), sticky="E")

        self.crossing_precision = self.create_spinbox(0, 10, 0.1, 28, "normal")
        self.crossing_precision.grid(row=10, column=0, padx=(0, 10), sticky="E")

        self.mutation_option = ttk.Combobox(self.right_scrollable_frame,
                                            values=("Brzegowa", "Jednopunktowa",
                                                    "Dwupunktowa"),
                                            width=20)
        self.mutation_option.set("-- Nie wybrano --")
        self.mutation_option.bind("<<ComboboxSelected>>", self.justamethod)
        self.mutation_option.grid(row=11, column=0, padx=(0, 18), sticky="E")

        self.mutation_precision = self.create_spinbox(0, 10, 0.1, 28, "normal")
        self.mutation_precision.grid(row=12, column=0, padx=(0, 10), sticky="E")

        self.inversion_precision = self.create_spinbox(0, 10, 0.1, 28, "normal")
        self.inversion_precision.grid(row=13, column=0, padx=(0, 10), sticky="E")

        self.population_procent = self.create_spinbox(0, 100, 1, 28, "disable")
        self.population_procent.grid(row=14, column=0, padx=(0, 10), sticky="E")

        self.normal_or_disabled()

        self.population_size = self.create_spinbox(0, 1000, 1, 28, "disable")
        self.population_size.grid(row=15, column=0, padx=(0, 10), sticky="E")

        self.button2 = Button(self.right_scrollable_frame, text="Start", bg=RIGHT_FRAME_FONT_COLOR, fg="white",
                              borderless=1,
                              takefocus=0, width=round(self.width * 0.55 - 100), command=self.plot)
        self.button2.grid(row=16, columnspan=2, pady=15, sticky="S")

    def set_lables_right_frame(self):
        self.crate_title_label(0)
        self.create_label("Przedział X1 funkcji", 2)
        self.create_label("Przedział X2 funkcji", 3)
        self.create_label("Dokładności chromosomu", 5)
        self.create_label("Wielkości populacji", 6)
        self.create_label("Liczba epok", 7)
        self.create_label("Metoda selekcji", 8)
        self.create_label("Krzyżowanie", 9)
        self.create_label("Prawdopodobieństwo krzyżowania", 10)
        self.create_label("Mutacja", 11)
        self.create_label("Prawdopodobieństwo mutacji", 12)
        self.create_label("Prawdopodobieństwo inwersji", 13)
        # self.create_label("Liczba zmiennych funkcji") -> 1,2,3,4,5
        # self.create_label("Wielkosc turnieju") -> 1,2,3,4,5
        # self.create_label("Procent osobnikow w Strategii elitarnej")
        # self.create_label("Liczba osobnikow w Strategii elitarnej")

        self.create_radio_button("Procent osobników", 3, self.method, 14, 1, "W")
        self.create_radio_button("Liczba osobników", 4, self.method, 15, 1, "W")

    def crate_title_label(self, row):
        return tk.Label(self.right_scrollable_frame,
                        text="Algorytm genetyczny znajdujący maks/min w Funkcji Beale",
                        font="system-ui 15 bold",
                        bg=RIGHT_FRAME_BACKGROUND_COLOR, fg=RIGHT_FRAME_TITLE_COLOR).grid(row=row, column=0, padx=20,
                                                                                          pady=5,
                                                                                          sticky="N")

    def create_label(self, title, row):
        return tk.Label(self.right_scrollable_frame,
                        text=title,
                        font="system-ui 12 bold",
                        bg=RIGHT_FRAME_BACKGROUND_COLOR, fg=RIGHT_FRAME_FONT_COLOR).grid(row=row, column=0, padx=20,
                                                                                         pady=10,
                                                                                         sticky="W")

    def create_spinbox(self, _from, _to, _increment, width, state):
        return tk.Spinbox(self.right_scrollable_frame, from_=_from, to=_to,
                          increment=_increment,
                          textvariable=tk.DoubleVar(value=0),
                          font="SYSTEM-UI 10",
                          bg="#FFFFFF",
                          fg='#000000',
                          width=width,
                          state=state)

    def create_radio_button(self, title, val, variable, row, column, place):
        s = ttk.Style()
        s.configure("Wild.TRadiobutton",
                    foreground=RIGHT_FRAME_FONT_COLOR,
                    font="system-ui 12 bold")

        return ttk.Radiobutton(self.right_scrollable_frame,
                               text=title,
                               style="Wild.TRadiobutton",
                               value=val, variable=variable,
                               command=lambda: self.clicked()).grid(row=row, columnspan=column, padx=(20, 20), pady=10,
                                                                    sticky=place)

    def justamethod(self, event):
        print("method is called: choosen -> ", self.selection_option.get())
        print("selection is called: choosen -> ", self.selection_option.get())
        print("crossing is called: choosen -> ", self.crossing_option.get())
        print("crossing is called: choosen -> ", self.mutation_option.get())
        print(" self.chromosome_precision, ", self.chromosome_precision.get())
        print(" self.population_procent", self.population_procent.get())
        print("self.mutation_precision", self.mutation_precision.get())

    def get_seletced_parameters(self):
        # w tej funkcji trzeba zwrocic wszystkie parametry ustawione
        # num_of_epochs
        # population_size
        # num_of_variables
        # range_min
        # range_max
        # precision
        # selection_type <- sa enumy w Helpers/enums.py
        # mutation_type
        # crossing_type
        # is_max <- czy szukamy min czy max funkcji
        # selection_prob
        # mutation_prob
        # crossing_prob
        # inversion_prob
        # tournament_size
        # selection_percent
        # elite_strategy_percent ALBO percent albo num jak uzytkownik ustawi dwa to do ktoregos trzeba dac 0 :)
        # elite_strategy_num
        return 50, 100, 2, -4, 4, 0.0001, SelectionType.ROULETTE, MutationType.SINGLE_POINT, CrossingType.SINGLE_POINT, False, 0.9, 0.1, 0.9, 0.1, 3, 80, 10, 0

    def clicked(self):
        self.normal_or_disabled()
        print(self.max_min_method.get())
        print(self.method.get())

    def normal_or_disabled(self):
        if self.method.get() == 3:
            self.population_procent.configure(state="normal")
            self.population_size.configure(state="disable")
        elif self.method.get() == 4:
            self.population_procent.configure(state="disable")
            self.population_size.configure(state="normal")

    def plot(self):
        # dodac Label z liczeniem czasu
        # czas start...
        algorithm = GeneticAlgorithm(bale_function, *self.get_seletced_parameters())
        best_solution_in_epochs, solution_mean, solution_std = algorithm.run_algorithm()
        # czas koniec
        # wyswietlic czas obliczen
        x = np.array([x+1 for x in range(0, len(best_solution_in_epochs))])
        # x to jest [1,2,3,4,6,7] itd kolejne epoki

        print(x)
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        p = np.array(
            [16.23697, 17.31653, 17.22094, 17.68631, 17.73641, 18.6368, 19.32125, 19.31756, 21.20247, 22.41444,
             22.11718, 22.12453])

        fig = Figure(figsize=(5, 5))
        a = fig.add_subplot(111)
        a.plot(p, range(2 + max(x)), color="blue")

        a.set_title("Estimation Grid", fontsize=12)
        a.set_ylabel("Y", fontsize=10)
        a.set_xlabel("X", fontsize=10)

        canvas0 = FigureCanvasTkAgg(fig, self.left_scrollable_frame)
        canvas0.get_tk_widget().grid(column=0, row=0)
        canvas0.draw()

        canvas1 = FigureCanvasTkAgg(fig, self.left_scrollable_frame)
        canvas1.get_tk_widget().grid(column=0, row=1)
        canvas1.draw()

        canvas2 = FigureCanvasTkAgg(fig, self.left_scrollable_frame)
        canvas2.get_tk_widget().grid(column=0, row=2)
        canvas2.draw()


if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()
