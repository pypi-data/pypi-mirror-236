from Jasonqwu import *


def login():
    name = username.get()
    pwd = password.get()
    if name == "admin" and pwd == "123456":
        debug(f"username = {name}, password = {pwd}")
    else:
        messagebox.showinfo("警告", "登录失败，请检查账号密码是否正确！")


root = Window("登录页", "300x180")
username = tkinter.StringVar()
password = tkinter.StringVar()

page = root.frame()
page.pack()
root.label(page).grid(row=0, column=0)

root.label(page, "账户： ").grid(row=1, column=1)
root.entry(page, textvariable=username).grid(row=1, column=2)

root.label(page, "密码： ").grid(row=2, column=1, pady=10)
root.entry(page, textvariable=password).grid(row=2, column=2)

root.button(page, login, "登录").grid(row=3, column=1, pady=10)
root.button(page, page.quit, "退出").grid(row=3, column=2)

root.window.mainloop()
