import tkinter as tk
from tkinter import ttk
from tkmacosx import Button


class MainApplication(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.width = self.master.winfo_screenwidth() / 1.5
        self.height = self.master.winfo_screenheight() / 1.5
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title("OE - Projekt nr 1")
        self.master.geometry("%ix%i" % (self.width, self.height))
        self.master.configure(bg="skyblue")
        self.master.resizable(0, 0)

    def create_widgets(self):
        self.create_frames()
        self.create_buttons()

    def create_frames(self):
        self.left_frame = tk.Frame(width=self.width * 0.65 - 20, height=self.height - 20, background='red')
        self.left_frame.grid_propagate(0)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.right_frame = tk.Frame(width=self.width * 0.35 - 20, height=self.height - 20, background='gold2')
        self.right_frame.grid_propagate(0)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)

    def create_buttons(self):
        self.create_left_frame_buttons()
        self.create_right_frame_buttons()

    def create_left_frame_buttons(self):
        self.button1 = Button(self.left_frame, text='Mac OSX', bg='black', fg='green', borderless=1)
        self.button1.grid(row=0, column=0, padx=30, pady=20)

        self.button2 = Button(self.left_frame, text='Button2', borderless=1)
        self.button2.grid(row=1, column=0, padx=30, pady=20)

    def create_right_frame_buttons(self):
        v = ["one", "two", "three", "four"]
        self.combo = ttk.Combobox(self.right_frame, values=v)
        self.combo.grid(row=0, column=0, padx=10, pady=10)
        self.combo.bind("<<ComboboxSelected>>", self.justamethod)

        self.button1 = Button(self.right_frame, text='Button3', borderless=1)
        self.button1.grid(row=1, column=0)

        self.button2 = Button(self.right_frame, text='Button4', borderless=1)
        self.button2.grid(row=1, column=1)

    def justamethod(self, event):
        print("method is called")
        print(self.combo.get())


if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()

# import matplotlib
# matplotlib.use('TkAgg')
# import numpy as np
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# from tkinter import *
#
# class mclass:
#     def __init__(self,  window):
#         self.window = window
#         self.box = Entry(window)
#         self.button = Button (window, text="check", command=self.plot)
#         self.box.pack ()
#         self.button.pack()
#
#     def plot (self):
#         x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#         v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
#         p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
#             19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])
#
#         fig = Figure(figsize=(6,6))
#         a = fig.add_subplot(111)
#         a.scatter(v,x,color='red')
#         a.plot(p, range(2 +max(x)),color='blue')
#         a.invert_yaxis()
#
#         a.set_title ("Estimation Grid", fontsize=16)
#         a.set_ylabel("Y", fontsize=14)
#         a.set_xlabel("X", fontsize=14)
#
#         canvas = FigureCanvasTkAgg(fig, master=self.window)
#         canvas.get_tk_widget().pack()
#         canvas.draw()
#
# window= Tk()
# start= mclass (window)
# window.mainloop()
