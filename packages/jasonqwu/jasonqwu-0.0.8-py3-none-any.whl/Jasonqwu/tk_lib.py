import tkinter
from tkinter import ttk
from tkinter import messagebox
from Jasonqwu import *


class Window:
    def __init__(self, title="tk", geometry=None):
        self.__counter = 0
        self.__window = tkinter.Tk()
        self.window.title(title)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        if geometry is None:
            geometry = f"{int(width / 2)}x{int(height / 2)}" \
                       + f"+{int(width / 4)}+{int(height / 4)}"
        self.window.geometry(geometry)
        self.__frame = []
        self.__label = []
        self.__entry = []
        self.__button = []
        self.__listbox = []

    @property
    def counter(self):
        return self.__counter

    @counter.setter
    def counter(self, value):
        self.__counter = value

    @property
    def window(self):
        return self.__window

    def frame(self):
        widget = tkinter.Frame(self.window)
        self.__frame.append(widget)
        return self.__frame[-1]

    def label(self, window, content="", padx=0, pady=0):
        widget = tkinter.Label(window,
                               text=content,
                               padx=padx,
                               pady=pady)
        self.__label.append(widget)
        return self.__label[-1]

    def entry(self, window, textvariable=""):
        widget = tkinter.Entry(window, textvariable=textvariable)
        self.__entry.append(widget)
        return self.__entry[-1]

    def button(self, window, function, content="", padx=0, pady=0):
        widget = tkinter.Button(window,
                                text=content,
                                command=function,
                                padx=padx,
                                pady=pady)
        # widget.bind("<Button-1>", function)
        self.__button.append(widget)
        return self.__button[-1]

    def listbox_append(self, number):
        for i in range(number):
            self.__listbox.append(tkinter.Listbox(self.window))
            debug(f"self.__listbox[{i}] = {self.__listbox[i]}")

    def set_listbox(self, index, value):
        self.__listbox[index].insert(0, value)
        self.__listbox[index].pack()

    def songhua(self):
        messagebox.showinfo("Message", "送你一朵玫瑰花，请你爱上我")
        debug("送你 99 朵玫瑰花")

    def run_counter(self, digit):
        def counting():
            self.counter += 1
            digit.config(text=str(self.counter))
            digit.after(1000, counting)

        counting()


if __name__ == '__main__':
    language = ["C", "python", "php", "html", "SQL", "java"]
    movie = ["CSS", "jQuery", "Bootstrap"]
    window = Window("Jason 的图形界面")
    window.label(window.window, "I like tkinter").pack()
    digit = window.label(window.window, "digit")
    window.run_counter(digit)
    digit.pack()
    window.button(window.window, window.songhua, "点我就送花").pack()
    window.listbox_append(2)
    for item in language:
        window.set_listbox(0, item)
    for item in movie:
        window.set_listbox(1, item)
    window.window.mainloop()
