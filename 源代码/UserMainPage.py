import pymysql
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox  # 弹窗


class UserMainPage:
    def __init__(self, parent_window, account) :
        self.account = account
        parent_window.destroy()  # 销毁主界面
        self.__parent_window__ = parent_window
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('用户系统')
        self.window.geometry('1024x700')  # 这里的乘是小x

        label = tk.Label(self.window, text='用户登陆', font=('宋体', 20), width=40, height=8)
        label.pack()

        Button(self.window, text="查询购买机票", font=tkFont.Font(size=16),
               command=lambda : UserFlightPage(self.window, self.account),
               width=40, height=2, fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text="查看已购买机票", font=tkFont.Font(size=16),
               command=lambda : Userbuy(self.window, self.account),
               width=40, height=2, fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()
        Button(self.window, text="修改个人信息", font=tkFont.Font(size=16),
               command=lambda : UserChange(self.window, self.account),
               width=40, height=2, fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()
        Button(self.window, text="退出", width=15, height=2, font=tkFont.Font(size=14), command=self.window.destroy).pack()

        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环


class Userbuy:
    def __init__(self, parent_window, account):
        self.account = account
        parent_window.destroy()  # 销毁主界面
        self.__parent_window__ = parent_window
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('本人机票')
        self.window.geometry('1024x700')  # 这里的乘是小x

        self.frame_top = tk.Frame(width=400, height=200)
        self.frame_center = tk.Frame(width=900, height=900)

        self.var_name = StringVar()
        self.var_sex = StringVar()
        self.var_age = StringVar()
        self.var_id_card = StringVar()
        self.var_tele = StringVar()

        # 定义下方中心列表区域
        self.columns = ("航班号", "日期", "出发机场", "出发时间", "到达机场", "到达时间", "航空公司", "座舱等级", "购买价格")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("航班号", width=70, anchor='center')  # 表示列,不显示
        self.tree.column("日期", width=70, anchor='center')
        self.tree.column("出发机场", width=130, anchor='center')
        self.tree.column("出发时间", width=70, anchor='center')
        self.tree.column("到达机场", width=130, anchor='center')
        self.tree.column("到达时间", width=70, anchor='center')
        self.tree.column("航空公司", width=70, anchor='center')
        self.tree.column("座舱等级", width=70, anchor='center')
        self.tree.column("购买价格", width=70, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.flight = []
        self.date = []
        self.depairport = []
        self.deptime = []
        self.arrtime = []
        self.arrairport = []
        self.aircompany = []
        self.cabin = []
        self.ticprice = []

        self.get_ticket()

        self.var_flight = StringVar()
        self.var_date = StringVar()
        self.var_cabin = StringVar()

        for i in range(len(self.flight)):  # 写入数据
            self.tree.insert('', i, values=(self.flight[i], self.date[i], self.depairport[i], self.deptime[i],
                                            self.arrairport[i], self.arrtime[i], self.aircompany[i], self.cabin[i],
                                            self.ticprice[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置

        # 右上区域设置
        self.right_top_title = Label(self.frame_top, text="操作：", font=('宋体', 20))
        self.right_top_button1 = ttk.Button(self.frame_top, text='退票', width=20, command=lambda: self.delete_ticket())
        self.right_top_button3 = ttk.Button(self.frame_top, text='返回', width=20, command=self.back)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=5)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=5)
        self.right_top_button3.grid(row=2, column=1, padx=20, pady=5)

        # 整体区域定位
        self.frame_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=50, pady=5)

        self.frame_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)

        self.frame_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def delete_ticket(self):
        if self.var_flight.get() == None:
            messagebox.showinfo('警告！', '请选择退票')
        else:
            db = pymysql.connect(host="localhost",
                                 user="root",
                                 password="sam20001207",
                                 database="air_ms")
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            # SQL 语句
            sql1 = "DELETE FROM user_purchase_info WHERE user_account = '%s' and flight_id = '%s'" \
                   "and flight_date = '%s'" % (self.account, self.var_flight.get(), self.var_date.get())
            if self.var_cabin.get() == 'Y 经济舱':
                sql2 = "UPDATE standby_ticket_info set yt_left = yt_left + 1 " \
                       "WHERE flight_id = '%s' and flight_date = '%s'"% (self.var_flight.get(), self.var_date.get())
            elif self.var_cabin.get() == 'C 商务舱':
                sql2 = "UPDATE standby_ticket_info set ct_left = ct_left + 1 " \
                       "WHERE flight_id = '%s' and flight_date = '%s'"% (self.var_flight.get(), self.var_date.get())
            else:
                sql2 = "UPDATE standby_ticket_info set ft_left = ft_left + 1 " \
                       "WHERE flight_id = '%s' and flight_date = '%s'"% (self.var_flight.get(), self.var_date.get())
            try:
                cursor.execute(sql2)  # 执行sql语句
                print("sql2")
                cursor.execute(sql1)  # 执行sql语句
                print("sql1")
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
            self.delButton(self.tree)
            self.get_ticket()

    def delButton(self, tree_1) :
        x = tree_1.get_children()
        for item in x :
            tree_1.delete(item)

    def click(self, event) :
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行
        self.row_info = self.tree.item(self.row, "values")
        self.var_flight.set(self.row_info[0])
        self.var_date.set(self.row_info[1])
        self.var_cabin.set(self.row_info[7])
        print('1')

    def get_ticket(self):
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        # SQL 语句
        sql = "select user_purchase_info.flight_id, user_purchase_info.flight_date, dep_airport_name, dep_time, " \
              "arr_airport_name, arr_time, air_company, " \
              "user_purchase_info.purchase_cabin, user_purchase_info.purchase_price " \
              "from user_purchase_info, flight_view " \
              "where user_purchase_info.user_account = '%s' " \
              "and user_purchase_info.flight_id = flight_view.flight_id " \
              "and user_purchase_info.flight_date = flight_view.flight_date;" % (self.account)
        print(self.account)
        try :
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            print(1)
            for row in results:
                self.flight.append(row[0])
                self.date.append(row[1])
                self.depairport.append(row[2])
                self.deptime.append(row[3])
                self.arrairport.append(row[4])
                self.arrtime.append(row[5])
                self.aircompany.append(row[6])
                self.cabin.append(row[7])
                self.ticprice.append(row[8])
            db.close()
        except :
            db.rollback()  # 发生错误时回滚
            messagebox.showinfo('错误！', '出错了！')


    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题


    def back(self):
        UserMainPage(self.window, self.account)  # 显示主窗口 销毁本窗口


class UserChange:
    def __init__(self, parent_window, account):
        parent_window.destroy()  # 销毁主界面
        self.account = account
        self.window = Tk()  # 初始框的声明
        self.window.title('用户信息')
        self.window.geometry('800x600')  # 这里的乘是小x

        self.frame_left_top = tk.Frame(width=400, height=600)
        self.frame_right_top = tk.Frame(width=200, height=200)
        self.frame_center = tk.Frame(width=600, height=400)

        self.var_name = StringVar()
        self.var_sex = StringVar()
        self.var_age = StringVar()
        self.var_id_card = StringVar()
        self.var_tele = StringVar()


        self.get_info()
        self.left_top_title = Label(self.frame_left_top, text="个人信息：", font=('宋体', 20))
        self.left_top_1_label = Label(self.frame_left_top, text="用户名：{}".format(self.account), font=('宋体', 15))
        self.left_top_1_label.grid(row=1, column=0, pady=10)  # 位置设置
        # 到达
        self.left_top_2_label = Label(self.frame_left_top, text="姓名：", font=('宋体', 15))
        self.left_top_2_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('宋体', 15))
        self.left_top_2_label.grid(row=2, column=0, pady=10)  # 位置设置
        self.left_top_2_entry.grid(row=2, column=1)
        # 日期
        self.left_top_3_label = Label(self.frame_left_top, text="性别：", font=('宋体', 15))
        self.left_top_3_entry = Entry(self.frame_left_top, textvariable=self.var_sex, font=('宋体', 15))
        self.left_top_3_label.grid(row=3, column=0, pady=10)  # 位置设置
        self.left_top_3_entry.grid(row=3, column=1)
        # 航班选择
        self.left_top_4_label = Label(self.frame_left_top, text="年龄", font=('宋体', 15))
        self.left_top_4_entry = Entry(self.frame_left_top, textvariable=self.var_age, font=('宋体', 15))
        self.left_top_4_label.grid(row=4, column=0, pady=10)  # 航班选择
        self.left_top_4_entry.grid(row=4, column=1)

        self.left_top_5_label = Label(self.frame_left_top, text="身份证号", font=('宋体', 15))
        self.left_top_5_entry = Entry(self.frame_left_top, textvariable=self.var_id_card, font=('宋体', 15))
        self.left_top_5_label.grid(row=5, column=0, pady=10)  # 航班选择
        self.left_top_5_entry.grid(row=5, column=1)

        self.left_top_6_label = Label(self.frame_left_top, text="电话号吗", font=('宋体', 15))
        self.left_top_6_entry = Entry(self.frame_left_top, textvariable=self.var_tele, font=('宋体', 15))
        self.left_top_6_label.grid(row=6, column=0, pady=10)  # 航班选择
        self.left_top_6_entry.grid(row=6, column=1)

        # 右上区域设置
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('宋体', 20))
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='修改', width=20, command=self.update_info)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='返回', width=20, command=self.back)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=5)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=5)
        self.right_top_button3.grid(row=3, column=0, padx=20, pady=5)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=5)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=50, pady=5)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def update_info(self):
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        # SQL 语句
        sql1 = "update user_info set user_name = '%s' where user_account = '%s'" % (self.var_name.get(),self.account)
        sql2 = "update user_info set sex = '%s' where user_account = '%s'" % (self.var_sex.get(),self.account)
        sql3 = "update user_info set age = %d where user_account = '%s'" % (int(self.var_age.get()), self.account)
        sql4 = "update user_info set identity_card = '%s' where user_account = '%s'" % (self.var_id_card.get(),self.account)
        sql5 = "update user_info set tele = '%s' where user_account = '%s'" % (self.var_tele.get(),self.account)

        print(self.account)
        try :
            cursor.execute(sql1)  # 执行sql语句
            cursor.execute(sql2)  # 执行sql语句
            cursor.execute(sql3)  # 执行sql语句
            cursor.execute(sql4)  # 执行sql语句
            cursor.execute(sql5)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            messagebox.showinfo('成功！', '个人信息修改成功！')
        except :
            db.rollback()  # 发生错误时回滚
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接
        self.get_info()

    def get_info(self):
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        # SQL 语句
        sql = "select * from user_info where user_account = '%s'" % (self.account)
        print(self.account)
        try :
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                if row[1] != None:
                    self.var_name.set(row[1])
                if row[2] != None :
                    self.var_sex.set(row[2])
                if row[3] != None :
                    self.var_age.set(row[3])
                if row[4] != None :
                    self.var_id_card.set(row[4])
                if row[5] != None :
                    self.var_tele.set(row[5])
            db.close()
        except :
            db.rollback()  # 发生错误时回滚
            messagebox.showinfo('错误！', '出错了！')

    def back(self):
        UserMainPage(self.window, self.account)  # 显示主窗口 销毁本窗口



class UserFlightPage:
    def __init__(self, parent_window, account):
        parent_window.destroy()  # 销毁主界面
        self.account = account
        self.window = Tk()  # 初始框的声明
        self.window.title('查询航班操作界面')
        self.window.geometry('1920x1080')  # 这里的乘是小x

        self.frame_left_top = tk.Frame(width=1024, height=300)
        self.frame_right_top = tk.Frame(width=200, height=300)
        self.frame_center = tk.Frame(width=1600, height=400)

        # 定义下方中心列表区域
        self.columns = ("航班代号", "出发机场", "到达机场", "出发时间", "到达时间", "航空公司", "执飞机型", "头等舱余票信息",
                        "商务舱余票信息", "经济舱余票信息")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=36, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("航班代号", width=100, anchor='center')  # 表示列,不显示
        self.tree.column("出发机场", width=120, anchor='center')
        self.tree.column("到达机场", width=120, anchor='center')
        self.tree.column("出发时间", width=70, anchor='center')
        self.tree.column("到达时间", width=70, anchor='center')
        self.tree.column("航空公司", width=70, anchor='center')
        self.tree.column("执飞机型", width=70, anchor='center')
        self.tree.column("头等舱余票信息", width=200, anchor='center')
        self.tree.column("商务舱余票信息", width=200, anchor='center')
        self.tree.column("经济舱余票信息", width=200, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)


        # 定义顶部区域

        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="航班信息:", font=('宋体', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_dep_city = StringVar()  # 声明出发
        self.var_arr_city = StringVar()  # 声明到达
        self.var_flight_date = StringVar()  # 声明日期
        self.var_flight_select = StringVar()  # 声明航班选择
        self.var_info1 = StringVar()
        self.var_info2 = StringVar()
        self.var_info3 = StringVar()
        # 出发
        self.left_top_1_label = Label(self.frame_left_top, text="出发城市：", font=('宋体', 15))
        self.left_top_1_entry = Entry(self.frame_left_top, textvariable=self.var_dep_city, font=('宋体', 15))
        self.left_top_1_label.grid(row=1, column=0)  # 位置设置
        self.left_top_1_entry.grid(row=1, column=1)
        # 到达
        self.left_top_2_label = Label(self.frame_left_top, text="到达城市：", font=('宋体', 15))
        self.left_top_2_entry = Entry(self.frame_left_top, textvariable=self.var_arr_city, font=('宋体', 15))
        self.left_top_2_label.grid(row=2, column=0)  # 位置设置
        self.left_top_2_entry.grid(row=2, column=1)
        # 日期
        self.left_top_3_label = Label(self.frame_left_top, text="日期：", font=('宋体', 15))
        self.left_top_3_entry = Entry(self.frame_left_top, textvariable=self.var_flight_date, font=('宋体', 15))
        self.left_top_3_label.grid(row=3, column=0)  # 位置设置
        self.left_top_3_entry.grid(row=3, column=1)
        # 航班选择
        self.left_top_4_label = Label(self.frame_left_top, text="已选航班",
                                      font=('宋体', 15))
        self.left_top_4_entry = Entry(self.frame_left_top, textvariable=self.var_flight_select, font=('宋体', 15))
        self.left_top_4_label.grid(row=4, column=0, pady=10)  # 航班选择
        self.left_top_4_entry.grid(row=4, column=1)
        self.left_top_button1 = ttk.Button(self.frame_left_top, text='购买头等舱', width=20,
                                           command=lambda: self.buy(1))
        self.left_top_button2 = ttk.Button(self.frame_left_top, text='购买商务舱', width=20,
                                           command=lambda: self.buy(2))
        self.left_top_button3 = ttk.Button(self.frame_left_top, text='购买经济舱', width=20,
                                           command=lambda: self.buy(3))
        self.left_top_button1.grid(row=5, column=0, padx=2, pady=25)
        self.left_top_button2.grid(row=5, column=1, padx=2, pady=25)
        self.left_top_button3.grid(row=5, column=2, padx=2, pady=25)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('宋体', 20))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='查询',  width=20, command=self.inquire)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='返回', width=20, command=self.back)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=5)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=5)
        self.right_top_button3.grid(row=3, column=0, padx=20, pady=5)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=5)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        UserMainPage(self.window, self.account)  # 显示主窗口 销毁本窗口

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_flight_select.set(self.row_info[0])
        self.var_info1.set(self.row_info[7])
        self.var_info2.set(self.row_info[8])
        self.var_info3.set(self.row_info[9])
        print('')

    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def buy(self, buynum):
        if self.var_info1.get() == '头等舱已卖完或没有设置' and buynum == 1:
            messagebox.showinfo('错误！', '头等舱已卖完或没有设置！')
        elif self.var_info2.get() == '商务舱已卖完或没有设置' and buynum == 2:
            messagebox.showinfo('错误！', '商务舱已卖完或没有设置！')
        elif self.var_info2.get() == '经济舱已卖完' and buynum == 3:
            messagebox.showinfo('错误！', '经济舱已卖完！')
        else:
            if self.var_flight_select.get() != '':
                db = pymysql.connect(host="localhost",
                                     user="root",
                                     password="sam20001207",
                                     database="air_ms")
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                # SQL 插入语句
                sql1 = "call buy_tick('%s', '%s', '%s', %d, @ret);" % \
                       (self.var_flight_select.get(), self.var_flight_date.get(), self.account, buynum)
                print(self.var_flight_select.get(), self.var_flight_date.get(), self.account, buynum)
                sql2 = "select  @ret"
                re_s = ''
                try :
                    cursor.execute(sql1)  # 执行sql语句
                    cursor.execute(sql2)  # 查询调用存储过程后返回的参数
                    for result in cursor.fetchall() :
                        re_s = result[0]
                except :
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('错误！', '购买错误！')
                print(re_s)
                if re_s == 'True' :
                    if buynum == 1:
                        messagebox.showinfo('成功！', '头等舱购买成功！')
                    if buynum == 2:
                        messagebox.showinfo('成功！', '商务舱购买成功！')
                    if buynum == 3:
                        messagebox.showinfo('成功！', '经济舱购买成功！')
                else :
                    messagebox.showinfo('错误！', '失败！')
                db.close()  # 关闭数据库连接

            else:
                messagebox.showinfo('警告！', '请选择航班')

    def delButton(self, tree_1) :
        x = tree_1.get_children()
        for item in x :
            tree_1.delete(item)

    def inquire(self):
        self.delButton(self.tree)
        self.flight_id = []
        self.dep_iata = []
        self.dep_city = []
        self.dep_airport_name = []
        self.arr_iata = []
        self.arr_city = []
        self.arr_airport_name = []
        self.dep_time = []
        self.arr_time = []
        self.air_company = []
        self.aircraft_type = []
        self.flight_date = []
        self.ft_left = []
        self.ft_price = []
        self.ct_left = []
        self.ct_price = []
        self.yt_left = []
        self.yt_price = []
        # 打开数据库连接
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM flight_view where dep_city = '%s' and arr_city = '%s' and flight_date = '%s'" \
              % (self.var_dep_city.get(), self.var_arr_city.get(), self.var_flight_date.get())  # SQL 查询语句
        try :
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results :
                self.flight_id.append(row[0])
                self.dep_iata.append(row[1])
                self.dep_city.append(row[2])
                self.dep_airport_name.append(row[3])
                self.arr_iata.append(row[4])
                self.arr_city.append(row[5])
                self.arr_airport_name.append(row[6])
                self.dep_time.append(row[7])
                self.arr_time.append(row[8])
                self.air_company.append(row[9])
                self.aircraft_type.append(row[10])
                self.flight_date.append(row[11])
                self.ft_left.append(row[12])
                self.ft_price.append(row[13])
                self.ct_left.append(row[14])
                self.ct_price.append(row[15])
                self.yt_left.append(row[16])
                self.yt_price.append(row[17])

        except :
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接
        "航班代号", "出发机场", "到达机场", "出发时间", "到达时间", "航空公司", "执飞机型", "余票信息"
        for i in range(len(self.flight_id)):  # 写入数据
            if self.ft_left[i] == None or self.ft_left[i] == 0:
                ticket_info_1 = '头等舱已卖完或没有设置'
            else:
                ticket_info_1 ='头等舱余票 {}张, 票价 {}RMB'.format(self.ft_left[i], self.ft_price[i])
            if self.ct_left[i] == None or self.ft_left[i] == 0:
                ticket_info_2 = '商务舱已卖完或没有设置'
            else:
                ticket_info_2 = '商务舱余票 {}张, 票价 {}RMB'.format(self.ct_left[i], self.ct_price[i])
            if self.yt_left[i] == 0:
                ticket_info_3 = '经济舱已卖完'
            else:
                ticket_info_3 = '经济舱余票 {}张, 票价 {}RMB'.format(self.yt_left[i], self.yt_price[i])
            self.tree.insert('', i, values=(self.flight_id[i], self.dep_airport_name[i], self.arr_airport_name[i],
                                            self.dep_time[i], self.arr_time[i], self.air_company[i],
                                            self.aircraft_type[i], ticket_info_1, ticket_info_2, ticket_info_3))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))



if __name__ == '__main__':
    window = tk.Tk()
    UserMainPage(window, '111i')
