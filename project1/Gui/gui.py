import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkmacosx import Button


class MainApplication(tk.Frame):
    right_scrollable_frame: Frame

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.box = tk.Entry(master)
        self.width = self.master.winfo_screenwidth() / 1.25
        self.height = self.master.winfo_screenheight() / 1.25

    def configure_gui(self):
        self.master.title("OE - Projekt nr 1")
        self.master.geometry("%ix%i" % (self.width, self.height))
        self.master.configure(bg="skyblue")
        # self.master.resizable(0, 0)

    def create_widgets(self):
        self.create_frames()

    def create_frames(self):
        self.left_frame = tk.Frame(width=self.width * 0.55, height=self.height - 20, background='red')
        self.left_frame.grid(row=0, column=0)
        self.set_canvas_to_left_frame()

        self.right_frame = tk.Frame(width=self.width * 0.45, height=self.height - 20, background='yellow')
        self.right_frame.grid(row=0, column=1)
        self.set_canvas_to_right_frame()

    def set_canvas_to_left_frame(self):
        left_canvas = tk.Canvas(self.left_frame, width=self.width * 0.55 - 15, height=self.height - 20,
                                highlightthickness=0,
                                background="white")

        left_scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=left_canvas.yview)
        self.left_scrollable_frame = ttk.Frame(left_canvas)

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
        right_canvas = tk.Canvas(self.right_frame, width=self.width * 0.45 - 15, height=self.height - 20,
                                 highlightthickness=0,
                                 background="#ECECEC")

        right_scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=right_canvas.yview)
        self.right_scrollable_frame = ttk.Frame(right_canvas)

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
        # v = ["one", "two", "three", "four"]
        # self.combo = ttk.Combobox(self.right_frame, values=v)
        # self.combo.grid(row=0, column=0, padx=10, pady=10)
        # self.combo.bind("<<ComboboxSelected>>", self.justamethod)
        #
        # self.button1 = Button(self.right_frame, text='Button3', borderless=1)
        # self.button1.grid(row=1, column=0)

        for i in range (40):
            self.button2 = ttk.Button(self.right_scrollable_frame, text='Button4', command=self.plot)
            self.button2.grid(row=i, column=1)

            self.button3 = ttk.Button(self.right_scrollable_frame, text='Button5', command=self.plot)
            self.button3.grid(row=i, column=2)

    def justamethod(self, event):
        print("method is called: choosen -> ", self.combo.get())

    def plot(self):
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        p = np.array([16.23697, 17.31653, 17.22094, 17.68631, 17.73641, 18.6368, 19.32125, 19.31756, 21.20247, 22.41444,
                      22.11718, 22.12453])

        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        a.plot(p, range(2 + max(x)), color='blue')

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


if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()
