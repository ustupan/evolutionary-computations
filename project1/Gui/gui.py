import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame
from tkmacosx import Button
from datetime import datetime
import time

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from project1.Algorithm.beale_function import bale_function
from project1.Algorithm.genetic_algorithm import GeneticAlgorithm
from project1.Helpers.enums import SelectionType, MutationType, CrossingType

LEFT_FRAME_BACKGROUND_COLOR = "#FFFFFF"
RIGHT_FRAME_BACKGROUND_COLOR = "#E5E5E5"
RIGHT_FRAME_TITLE_COLOR = "#104FAF"
RIGHT_FRAME_FONT_COLOR = "#1872FB"

SELECTION_TYPE = ["Selekcja najlepszych", "Koło ruletki", "Selekcja turniejowa"]
CROSSING_TYPE = ["Jednopunktowe", "Dwupunktowe", "Trzypunktowe", "Jednorodne"]
MUTATION_TYPE = ["Brzegowa", "Jednopunktowa", "Dwupunktowa"]


class MainApplication(tk.Frame):
    right_scrollable_frame: Frame

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.box = tk.Entry(master)
        self.width = self.master.winfo_screenwidth() / 1.45
        self.height = self.master.winfo_screenheight() / 1.25
        self.max_min_method = tk.BooleanVar()
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
        self.create_radio_button("Maksymalizacja", True, self.max_min_method, 1, 1, "W")
        self.create_radio_button("Minimalizacja", False, self.max_min_method, 1, 1, "E")

        self.range_min = self.create_spinbox(-100, 100, 1, 11, "normal")
        self.range_min.grid(row=2, column=0, padx=(0, 112), sticky="E")

        self.range_max = self.create_spinbox(-100, 100, 1, 11, "normal")
        self.range_max.grid(row=2, column=0, padx=(0, 10), sticky="E")

        self.chromosome_precision = self.create_spinbox(0, 1, 0.01, 28, "normal")
        self.chromosome_precision.grid(row=3, column=0, padx=(0, 10), sticky="E")

        self.population_size = self.create_spinbox(0, 1000, 1, 28, "normal")
        self.population_size.grid(row=4, column=0, padx=(0, 10), sticky="E")

        self.num_of_epochs = self.create_spinbox(0, 1000, 1, 28, "normal")
        self.num_of_epochs.grid(row=5, column=0, padx=(0, 10), sticky="E")

        self.selection_option = ttk.Combobox(self.right_scrollable_frame, values=SELECTION_TYPE, width=20)
        self.selection_option.set("-- Nie wybrano --")
        self.selection_option.grid(row=6, column=0, padx=(0, 18), sticky="E")

        self.crossing_option = ttk.Combobox(self.right_scrollable_frame, values=CROSSING_TYPE, width=20)
        self.crossing_option.set("-- Nie wybrano --")
        self.crossing_option.grid(row=7, column=0, padx=(0, 18), sticky="E")

        self.crossing_precision = self.create_spinbox(0, 10, 0.1, 28, "normal")
        self.crossing_precision.grid(row=8, column=0, padx=(0, 10), sticky="E")

        self.mutation_option = ttk.Combobox(self.right_scrollable_frame, values=MUTATION_TYPE, width=20)
        self.mutation_option.set("-- Nie wybrano --")
        self.mutation_option.grid(row=9, column=0, padx=(0, 18), sticky="E")

        self.mutation_precision = self.create_spinbox(0, 10, 0.1, 28, "normal")
        self.mutation_precision.grid(row=10, column=0, padx=(0, 10), sticky="E")

        self.inversion_precision = self.create_spinbox(0, 10, 0.1, 28, "normal")
        self.inversion_precision.grid(row=11, column=0, padx=(0, 10), sticky="E")

        self.num_of_function_variables = self.create_spinbox(0, 1000, 1, 28, "normal")
        self.num_of_function_variables.grid(row=12, column=0, padx=(0, 10), sticky="E")

        self.tournament_size = self.create_spinbox(0, 1000, 1, 28, "normal")
        self.tournament_size.grid(row=13, column=0, padx=(0, 10), sticky="E")

        self.population_procent = self.create_spinbox(0, 100, 1, 28, "normal")
        self.population_procent.grid(row=14, column=0, padx=(0, 10), sticky="E")

        self.elit_strategy_population_procent = self.create_spinbox(0, 100, 1, 28, "disable")
        self.elit_strategy_population_procent.grid(row=15, column=0, padx=(0, 10), sticky="E")

        self.elit_strategy_population_size = self.create_spinbox(0, 1000, 1, 28, "disable")
        self.elit_strategy_population_size.grid(row=16, column=0, padx=(0, 10), sticky="E")

        self.button2 = Button(self.right_scrollable_frame, text="Start", bg=RIGHT_FRAME_FONT_COLOR, fg="white",
                              borderless=1,
                              takefocus=0, width=round(self.width * 0.55 - 100), command=self.plot)
        self.button2.grid(row=20, columnspan=2, pady=15, sticky="S")

    def set_lables_right_frame(self):
        self.crate_title_label(0)
        self.create_label("Przedział funkcji", 2)
        self.create_label("Dokładność chromosomu", 3)
        self.create_label("Wielkość populacji", 4)
        self.create_label("Liczba epok", 5)
        self.create_label("Metoda selekcji", 6)
        self.create_label("Krzyżowanie", 7)
        self.create_label("Prawdopodobieństwo krzyżowania", 8)
        self.create_label("Mutacja", 9)
        self.create_label("Prawdopodobieństwo mutacji", 10)
        self.create_label("Prawdopodobieństwo inwersji", 11)
        self.create_label("Liczba zmiennych funkcji", 12)
        self.create_label("Wielkość turnieju", 13)
        self.create_label("Procent osobników", 14)
        self.create_radio_button("Procent osobników (Strategia elitarna)", 1, self.method, 15, 1, "W")
        self.create_radio_button("Liczba osobników (Strategia elitarna)", 2, self.method, 16, 1, "W")

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

    def create_time_label(self, text):
        self.time_label = tk.Label(self.right_scrollable_frame, text="Obliczenia wykonały się w : %.5g sekund" % text, font="system-ui 12 bold",
                                   bg=RIGHT_FRAME_BACKGROUND_COLOR, fg=RIGHT_FRAME_FONT_COLOR).grid(row=19, column=0,
                                                                                                    padx=20, pady=10,
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
                               command=lambda: self.normal_or_disabled()).grid(row=row, columnspan=column,
                                                                               padx=(20, 20), pady=10,
                                                                               sticky=place)

    def get_seletced_parameters(self):
        # w tej funkcji trzeba zwrocic wszystkie parametry ustawione
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
        is_max = self.max_min_method.get()
        from_x1 = self.range_min.get()
        to_x1 = self.range_max.get()
        chrom_precision = self.chromosome_precision.get()
        pop_size = self.population_size.get()
        epoch_num = self.num_of_epochs.get()
        select_type = self.selection_option.get()
        cross_type = self.crossing_option.get()
        cross_precision = self.crossing_precision.get()
        mut_type = self.mutation_option.get()
        mut_precision = self.mutation_precision.get()
        invers_precision = self.inversion_precision.get()
        fun_variables_num = self.num_of_function_variables.get()
        tour_size = self.tournament_size.get()
        elit_strategy_pop_procent = self.elit_strategy_population_procent.get()
        elit_strategy_pop_size = self.elit_strategy_population_size.get()
        pop_procent = self.population_procent.get()

        for i in range(len(SELECTION_TYPE)):
            if select_type == SELECTION_TYPE[i]:
                select_type = SelectionType(i + 1)

        for i in range(len(CROSSING_TYPE)):
            if cross_type == CROSSING_TYPE[i]:
                cross_type = CrossingType(i + 1)

        for i in range(len(MUTATION_TYPE)):
            if mut_type == MUTATION_TYPE[i]:
                mut_type = MutationType(i + 1)

        # print(is_max)
        # print(from_x1)
        # print(to_x1)
        # print(chrom_precision)
        # print(pop_size)
        # print(epoch_num)
        # print(select_type)
        # print(cross_type)
        # print(cross_precision)
        # print(mut_type)
        # print(mut_precision)
        # print(invers_precision)
        # print(fun_variables_num)
        # print(tour_size)
        # print(elit_strategy_pop_procent)
        # print(elit_strategy_pop_size)
        # print(pop_procent)
        # print(pop_checkbox_size)

        return int(epoch_num), int(pop_size), int(fun_variables_num), int(from_x1), int(
            to_x1), float(chrom_precision), select_type, mut_type, cross_type, is_max, float(1), float(
            mut_precision), float(cross_precision), float(invers_precision), int(tour_size), int(pop_procent), int(
            elit_strategy_pop_procent), int(elit_strategy_pop_size)

    def normal_or_disabled(self):
        if self.method.get() == 1:
            self.elit_strategy_population_procent.configure(state="normal")
            self.elit_strategy_population_size.configure(state="disable")
        elif self.method.get() == 2:
            self.elit_strategy_population_procent.configure(state="disable")
            self.elit_strategy_population_size.configure(state="normal")

    def plot(self):
        start_time = datetime.now()
        algorithm = GeneticAlgorithm(bale_function, *self.clicked())
        best_solution_in_epochs, solution_mean, solution_std = algorithm.run_algorithm()
        print(len(best_solution_in_epochs))
        print(len(solution_mean))
        print(len(solution_std))
        end_time = datetime.now()

        self.create_time_label((end_time - start_time).total_seconds())

        x = np.array([x + 1 for x in range(0, len(solution_std))])
        p = np.array(solution_std)


        fig = Figure(figsize=(5, 5))
        a = fig.add_subplot(111)

        a.plot(x, p, color="blue")

        a.set_title("Wartość najlepszego osobnika w epoce", fontsize=12)
        a.set_ylabel("Y", fontsize=10)
        a.set_xlabel("X", fontsize=10)

        canvas0 = FigureCanvasTkAgg(fig, self.left_scrollable_frame)
        canvas0.get_tk_widget().grid(column=0, row=0)
        canvas0.draw()

        # canvas1 = FigureCanvasTkAgg(fig, self.left_scrollable_frame)
        # canvas1.get_tk_widget().grid(column=0, row=1)
        # canvas1.draw()
        #
        # canvas2 = FigureCanvasTkAgg(fig, self.left_scrollable_frame)
        # canvas2.get_tk_widget().grid(column=0, row=2)
        # canvas2.draw()


if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()
