import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
# from main import StartPage


class AboutPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('软件说明')
        self.window.geometry('1020x600')  # 这里的乘是小x

        label = tk.Label(self.window, text='软件使用说明', font=('宋体', 20), width=40, height=4)
        label.pack()

        Label(self.window, text='本系统用于飞机订票系统，通过系统对air_ms数据库的增删改查功能完成各种操作',
              font=('宋体', 20)).pack(pady=5)
        Label(self.window, text='1.通过管理员登录功能可以增加，删除，修改航班信息', font=('宋体', 12)).pack(pady=5)
        Label(self.window, text='2.通过管理员登录功能可以增加，删除机场信息', font=('宋体', 12)).pack(pady=5)
        Label(self.window, text='3.通过管理员登录功能可以修改用户已购买机票', font=('宋体', 12)).pack(pady=5)
        Label(self.window, text='4.通过用户登录功能可以查看航班信息', font=('宋体', 12)).pack(pady=5)
        Label(self.window, text='5.通过用户登录功能可以修改个人信息', font=('宋体', 12)).pack(pady=5)
        Label(self.window, text='6.通过用户登录功能可以购买机票', font=('宋体', 12)).pack(pady=5)
        Label(self.window, text='7.通过用户登录功能可以查询、取消已购买机票', font=('宋体', 12)).pack(pady=5)
        Label(self.window, text='8.通过用户登录功能可以创建新用户', font=('宋体', 12)).pack(pady=5)


        Label(self.window, text='版权：2020西工大数据库系统课程大作业', font=('宋体', 12)).pack(pady=5)
        Label(self.window, text='   ', font=('宋体', 12)).pack(pady=5)

        Label(self.window, text='软件作者：王澍   学号：2019302495 ', font=('宋体', 12)).pack(pady=5)

        Button(self.window, text="返回", width=8, font=tkFont.Font(size=12), command=self.back).pack(pady=100)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        # StartPage(self.window)  # 显示主窗口 销毁本窗口
        self.window.destroy()