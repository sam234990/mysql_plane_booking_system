import time
import os
import pymysql
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox  # 弹窗
from AdminMainPage import *
from UserMainPage import *

class StartPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁子界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('飞机订票系统')
        self.window.geometry('1024x700')  # 这里的乘是小x

        label = Label(self.window, text="飞机订票系统", font=("宋体", 20))
        label.pack(pady=100)  # pady=100 界面的长度

        Button(self.window, text="管理员登陆", font=tkFont.Font(size=16), command=lambda: AdminPage(self.window),
               width=40, height=2, fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text="用户登陆", font=tkFont.Font(size=16), command=lambda: UserPage(self.window),
               width=40, height=2,  fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text="使用说明和开发说明", font=tkFont.Font(size=16), command=lambda: AboutPage(self.window),
               width=40, height=2, fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text='退出', height=2, font=tkFont.Font(size=16), width=40, command=self.window.destroy,
               fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        self.window.mainloop()  # 主消息循环


class AboutPage:
    def __init__(self, parent_window):

        self.parent_window = parent_window
        parent_window.destroy()  # 销毁主界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('软件说明')
        self.window.geometry('1024x800')  # 这里的乘是小x

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
        StartPage(self.window)  # 显示主窗口 销毁本窗口


class AdminPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面
        self.__parent_window__ = parent_window
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员登陆页面')
        self.window.geometry('1024x700')  # 这里的乘是小x
        self.admin_id = ''
        self.admin_password = ''
        label = tk.Label(self.window, text='管理员登陆', font=('宋体', 20), width=40, height=8)
        label.pack()

        Label(self.window, text='用户名                                     ', font=tkFont.Font(size=14)).pack(pady=25)
        self.admin_username = tk.Entry(self.window, width=30, font=tkFont.Font(size=20), bg='white')
        self.admin_username.pack()

        Label(self.window, text='密码                                       ', font=tkFont.Font(size=14)).pack(pady=25)
        self.admin_pass = tk.Entry(self.window, width=30, font=tkFont.Font(size=20), bg='white', show='*')
        self.admin_pass.pack()

        Button(self.window, text="登陆", width=15, height=2, 
               font=tkFont.Font(size=14), command=self.login).pack(pady=40)
        Button(self.window, text="返回", width=15, height=2, font=tkFont.Font(size=14), command=self.back).pack()

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def login(self):
        print(str(self.admin_username.get()))
        print(str(self.admin_pass.get()))
        admin_pass = None

        # 数据库操作 查询管理员表
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms") # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM admin_login WHERE admin_id = '%d'" % (int(self.admin_username.get()))  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.admin_id = row[0]
                self.admin_password = row[1]
                # 打印结果
                print("admin_id=%s,admin_pass=%s" % (self.admin_id, self.admin_password))
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '用户名或密码不正确！')
        db.close()  # 关闭数据库连接

        print("正在登陆管理员管理界面")
        print("self", self.admin_pass.get())
        print("local", self.admin_password)
        # messagebox.showinfo('提示','正在登陆管理员管理界面')
        # time.sleep(5);

        if self.admin_pass.get() == self.admin_password:
            messagebox.showinfo('successful', '登录成功')
            AdminMainPage(self.window)  # 进入管理员操作界面
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口


class UserPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面
        self.__parent_window__ = parent_window
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('用户登陆页面')
        self.window.geometry('1024x700')  # 这里的乘是小x
        self.user_id = ''
        self.user_password = ''
        label = tk.Label(self.window, text='用户登陆', font=('宋体', 20), width=40, height=8)
        label.pack()

        Label(self.window, text='用户名                                     ', font=tkFont.Font(size=14)).pack(pady=25)
        self.username = tk.Entry(self.window, width=30, font=tkFont.Font(size=20), bg='white')
        self.username.pack()

        Label(self.window, text='密码                                       ',
              font=tkFont.Font(size=14)).pack(pady=25)
        self.password = tk.Entry(self.window, width=30, font=tkFont.Font(size=20), bg='white', show='*')
        self.password.pack()

        Button(self.window, text="登陆", width=15, height=2,
               font=tkFont.Font(size=14), command=self.login).pack(pady=10)
        Button(self.window, text="返回", width=15, height=2,
               font=tkFont.Font(size=14), command=self.back).pack(pady=10)
        Button(self.window, text="还没有账号？使用当前账户名密码来注册！", width=50, height=2,
               font=tkFont.Font(size=14), command=self.register).pack(pady=20)


        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def register(self):
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        re_s = ''
        sql = "call create_new_account('%s', '%s', '%s', @retw)" % \
              (str(self.username.get()), str(self.password.get()), str(self.password.get() + 'i'))
        try :
            # 执行SQL语句
            cursor.execute(sql)
            cursor.execute("select @retw")  # 查询调用存储过程后返回的参数
            for result in cursor.fetchall():
                re_s = result[0]
        except:
            messagebox.showinfo('警告！', '用户名或密码不正确！')
        print(re_s)
        if re_s == 'True':
            UserMainPage(self.window, str(self.password.get() + 'i')) # 进入用户操作界面
        else:
            print('fail')

    def login(self):
        print(str(self.username.get()))
        print(str(self.password.get()))
        admin_pass = None

        # 数据库操作 查询用户表
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms") # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM passenger_login WHERE passenger_id = '%s'" % (self.username.get())  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.user_id = row[0]
                self.user_password = row[1]
                # 打印结果
                print("admin_id=%s,admin_pass=%s" % (self.user_id, self.user_password))
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '用户名或密码不正确！')
        db.close()  # 关闭数据库连接

        print("正在登陆管理员管理界面")
        print("self", self.password.get())
        print("local", self.user_password)
        # messagebox.showinfo('提示','正在登陆用户界面')
        # time.sleep(5);

        if self.password.get() == self.user_password:
            # messagebox.showinfo('successful', '登录成功')
            UserMainPage(self.window, self.username.get() + 'i')  # 进入用户操作界面
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口


if __name__ == '__main__':
    try:
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 关闭数据库连接
        db.close()
        window = tk.Tk()
        StartPage(window)
    except :
        messagebox.showinfo('错误', '连接数据库失败！')
