import tkinter
from tkinter import messagebox
from Jasonqwu import *


class Window:
    def __init__(self, title="tk", geometry="450x300+100+100"):
        self.__window = tkinter.Tk()
        self.window.title(title)
        self.window.geometry(geometry)
        self.__button = []
        self.__listbox = []

    @property
    def window(self):
        return self.__window

    def button(self, content=""):
        btn = tkinter.Button(self.window)
        btn["text"] = content
        btn.pack()
        btn.bind("<Button-1>", self.songhua)
        self.__button.append(btn)

    def listbox_append(self, number):
        for i in range(number):
            self.__listbox.append(tkinter.Listbox(self.window))
            debug(f"self.__listbox[{i}] = {self.__listbox[i]}")

    def set_listbox(self, index, value):
        self.__listbox[index].insert(0, value)
        self.__listbox[index].pack()

    def songhua(self, event):
        messagebox.showinfo("Message", "送你一朵玫瑰花，请你爱上我")
        debug("送你 99 朵玫瑰花")


if __name__ == '__main__':
    language = ["C", "python", "php", "html", "SQL", "java"]
    movie = ["CSS", "jQuery", "Bootstrap"]
    window = Window("Jason 的图形界面", "500x400+300-250")
    window.button("点我就送花")
    window.listbox_append(2)
    for item in language:
        window.set_listbox(0, item)
    for item in movie:
        window.set_listbox(1, item)
    window.window.mainloop()
