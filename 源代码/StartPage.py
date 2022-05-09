import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
from main import StartPage

class StartPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁子界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('飞机订票系统')
        self.window.geometry('1024x700')  # 这里的乘是小x

        label = Label(self.window, text="飞机订票系统", font=("宋体", 20))
        label.pack(pady=100)  # pady=100 界面的长度

        Button(self.window, text="管理员登陆", font=tkFont.Font(size=16), command=lambda: AdminPage(self.window), width=40,
               height=2,
               fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        label = Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text="用户登陆", font=tkFont.Font(size=16), command=lambda: StudentPage(self.window), width=40,
               height=2,  fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        label = Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text="使用说明和开发说明", font=tkFont.Font(size=16), command=lambda: AboutPage(self.window), width=40,
               height=2,
               fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        label = Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text='退出', height=2, font=tkFont.Font(size=16), width=40, command=self.window.destroy,
               fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()


        self.window.mainloop()  # 主消息循环