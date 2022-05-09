import pymysql
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import tkinter.messagebox as messagebox  # 弹窗


class AdminMainPage:
    def __init__(self, parent_window) :
        parent_window.destroy()  # 销毁主界面
        self.__parent_window__ = parent_window
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员系统')
        self.window.geometry('1024x700')  # 这里的乘是小x

        label = tk.Label(self.window, text='管理员登陆', font=('宋体', 20), width=40, height=8)
        label.pack()

        Button(self.window, text="航班信息", font=tkFont.Font(size=16), command=lambda : AdminFlightPage(self.window),
               width=40, height=2, fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text="机场信息", font=tkFont.Font(size=16), command=lambda : AdminAirportPage(self.window),
               width=40, height=2, fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()

        Button(self.window, text="用户已购买机票", font=tkFont.Font(size=16),
               command=lambda : Adminbuy(self.window),
               width=40, height=2, fg='black', bg='white', activebackground='yellow', activeforeground='red').pack()
        Label(self.window, text=" ", font=("宋体", 20)).pack()
        Button(self.window, text="退出", width=15, height=2, font=tkFont.Font(size=14), command=self.window.destroy).pack()

        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环


class AdminFlightPage:
    def __init__(self, parent_window) :
        parent_window.destroy()  # 销毁主界面
        self.__parent_window__ = parent_window
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('航班信息')
        self.window.geometry('1024x700')  # 这里的乘是小x

        self.frame_left_top = tk.Frame(width=600, height=300)
        self.frame_right_top = tk.Frame(width=400, height=300)
        self.frame_center = tk.Frame(width=1024, height=900)

        self.var_name = StringVar()
        self.var_sex = StringVar()
        self.var_age = StringVar()
        self.var_id_card = StringVar()
        self.var_tele = StringVar()

        # 定义下方中心列表区域
        self.columns = ("航班号", "日期", "f余票", "f票价", "c余票", "c票价", "y余票", "y票价", )
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("航班号", width=70, anchor='center')  # 表示列,不显示
        self.tree.column("日期", width=150, anchor='center')
        self.tree.column("f余票", width=70, anchor='center')
        self.tree.column("f票价", width=70, anchor='center')
        self.tree.column("c余票", width=70, anchor='center')
        self.tree.column("c票价", width=70, anchor='center')
        self.tree.column("y余票", width=70, anchor='center')
        self.tree.column("y票价", width=70, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.flight = []
        self.date = []
        self.fle = []
        self.fpr = []
        self.cle = []
        self.cpr = []
        self.yle = []
        self.ypr = []

        self.get_ticket()

        self.var_flight = StringVar()
        self.var_date = StringVar()
        self.var_fle = StringVar()
        self.var_fpr = StringVar()
        self.var_cle = StringVar()
        self.var_cpr = StringVar()
        self.var_yle = StringVar()
        self.var_ypr = StringVar()


        self.tree.bind('<Button-1>', self.click)  # 左键获取位置

        # 机场代号
        self.left_top_1_label = Label(self.frame_left_top, text="航班号：", font=('宋体', 15))
        self.left_top_1_entry = Entry(self.frame_left_top, textvariable=self.var_flight, font=('宋体', 15))
        self.left_top_1_label.grid(row=1, column=0)  # 位置设置
        self.left_top_1_entry.grid(row=1, column=1)
        # 所在城市
        self.left_top_2_label = Label(self.frame_left_top, text="日期：", font=('宋体', 15))
        self.left_top_2_entry = Entry(self.frame_left_top, textvariable=self.var_date, font=('宋体', 15))
        self.left_top_2_label.grid(row=2, column=0)  # 位置设置
        self.left_top_2_entry.grid(row=2, column=1)
        # 机场名称
        self.left_top_3_label = Label(self.frame_left_top, text="f余票：", font=('宋体', 15))
        self.left_top_3_entry = Entry(self.frame_left_top, textvariable=self.var_fle, font=('宋体', 15))
        self.left_top_3_label.grid(row=3, column=0)  # 位置设置
        self.left_top_3_entry.grid(row=3, column=1)
        # 所在位置
        self.left_top_4_label = Label(self.frame_left_top, text="f票价：", font=('宋体', 15))
        self.left_top_4_entry = Entry(self.frame_left_top, textvariable=self.var_fpr, font=('宋体', 15))
        self.left_top_4_label.grid(row=4, column=0)  # 位置设置
        self.left_top_4_entry.grid(row=4, column=1)
        # 机场名称
        self.left_top_5_label = Label(self.frame_left_top, text="c余票：", font=('宋体', 15))
        self.left_top_5_entry = Entry(self.frame_left_top, textvariable=self.var_cle, font=('宋体', 15))
        self.left_top_5_label.grid(row=5, column=0)  # 位置设置
        self.left_top_5_entry.grid(row=5, column=1)
        # 所在位置
        self.left_top_6_label = Label(self.frame_left_top, text="c票价：", font=('宋体', 15))
        self.left_top_6_entry = Entry(self.frame_left_top, textvariable=self.var_cpr, font=('宋体', 15))
        self.left_top_6_label.grid(row=6, column=0)  # 位置设置
        self.left_top_6_entry.grid(row=6, column=1)# 机场名称

        self.left_top_7_label = Label(self.frame_left_top, text="y余票：", font=('宋体', 15))
        self.left_top_7_entry = Entry(self.frame_left_top, textvariable=self.var_yle, font=('宋体', 15))
        self.left_top_7_label.grid(row=7, column=0)  # 位置设置
        self.left_top_7_entry.grid(row=7, column=1)
        # 所在位置
        self.left_top_8_label = Label(self.frame_left_top, text="y票价：", font=('宋体', 15))
        self.left_top_8_entry = Entry(self.frame_left_top, textvariable=self.var_ypr, font=('宋体', 15))
        self.left_top_8_label.grid(row=8, column=0)  # 位置设置
        self.left_top_8_entry.grid(row=8, column=1)

        # 右上区域设置
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('宋体', 20))
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='修改', width=20, command=lambda :
        self.update_sch())
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='返回', width=20, command=self.back)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=5)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=5)
        self.right_top_button3.grid(row=2, column=1, padx=20, pady=5)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=5)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)

        self.frame_left_top.tkraise()
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def update_sch(self) :
        if self.var_flight.get() == None :
            messagebox.showinfo('警告！', '请选择')
        else :
            db = pymysql.connect(host="localhost",
                                 user="root",
                                 password="sam20001207",
                                 database="air_ms")
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql1 = "update standby_ticket_info set ft_left = '%s' where flight_id = '%s' and flight_date = '%s'" % (
            self.var_fle.get(), self.var_flight.get(), self.var_date.get())
            sql2 = "update standby_ticket_info set ft_price = '%s' where flight_id = '%s' and flight_date = '%s'" % (
            self.var_fpr.get(), self.var_flight.get(), self.var_date.get())
            sql3 = "update standby_ticket_info set ct_left = '%s' where flight_id = '%s' and flight_date = '%s'" % (
            self.var_cle.get(), self.var_flight.get(), self.var_date.get())
            sql4 = "update standby_ticket_info set ct_price = '%s' where flight_id = '%s' and flight_date = '%s'" % (
            self.var_cpr.get(), self.var_flight.get(), self.var_date.get())
            sql5 = "update standby_ticket_info set yt_left = '%s' where flight_id = '%s' and flight_date = '%s'" % (
            self.var_yle.get(), self.var_flight.get(), self.var_date.get())
            sql6 = "update standby_ticket_info set yt_price = '%s' where flight_id = '%s' and flight_date = '%s'" % (
            self.var_ypr.get(), self.var_flight.get(), self.var_date.get())
            try:
                if self.row_info[2] != self.var_fle.get():
                    cursor.execute(sql1)  # 执行sql语句
                if self.row_info[3] != self.var_fpr.get() :
                    cursor.execute(sql2)  # 执行sql语句
                if self.row_info[4] != self.var_cle.get():
                    cursor.execute(sql3)  # 执行sql语句
                if self.row_info[5] != self.var_cpr.get() :
                    cursor.execute(sql4)  # 执行sql语句
                if self.row_info[6] != self.var_yle.get():
                    cursor.execute(sql5)  # 执行sql语句
                if self.row_info[7] != self.var_ypr.get() :
                    cursor.execute(sql6)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('成功！', '信息修改成功！')
            except :
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()  # 关闭数据库连接


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
        self.var_fle.set(self.row_info[2])
        self.var_fpr.set(self.row_info[3])
        self.var_cle.set(self.row_info[4])
        self.var_cpr.set(self.row_info[5])
        self.var_yle.set(self.row_info[6])
        self.var_ypr.set(self.row_info[7])
        print('1')

    def get_ticket(self) :
        self.delButton(self.tree)
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        # SQL 语句
        sql = "select * from standby_ticket_info;"
        try :
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results :
                self.flight.append(row[0])
                self.date.append(row[1])
                self.fle.append(row[2])
                self.fpr.append(row[3])
                self.cle.append(row[4])
                self.cpr.append(row[5])
                self.yle.append(row[6])
                self.ypr.append(row[7])
            db.close()
        except :
            db.rollback()  # 发生错误时回滚
            messagebox.showinfo('错误！', '出错了！')
        for i in range(len(self.flight)) :  # 写入数据
            self.tree.insert('', i, values=(self.flight[i], self.date[i], self.fle[i], self.fpr[i]
                                            , self.cle[i], self.cpr[i], self.yle[i], self.ypr[i]))

        for col in self.columns :  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col : self.tree_sort_column(self.tree, _col, False))

    def tree_sort_column(self, tv, col, reverse) :  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l) :  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda : self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def back(self) :
        AdminMainPage(self.window)  # 显示主窗口 销毁本窗口


class Adminbuy:
    def __init__(self, parent_window) :
        parent_window.destroy()  # 销毁主界面
        self.__parent_window__ = parent_window
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('用户购买机票')
        self.window.geometry('1024x700')  # 这里的乘是小x

        self.frame_left_top = tk.Frame(width=600, height=300)
        self.frame_right_top = tk.Frame(width=400, height=300)
        self.frame_center = tk.Frame(width=1024, height=900)

        self.var_name = StringVar()
        self.var_sex = StringVar()
        self.var_age = StringVar()
        self.var_id_card = StringVar()
        self.var_tele = StringVar()

        # 定义下方中心列表区域
        self.columns = ("航班号", "日期", "用户名", "座舱等级")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("航班号", width=70, anchor='center')  # 表示列,不显示
        self.tree.column("日期", width=150, anchor='center')
        self.tree.column("用户名", width=150, anchor='center')
        self.tree.column("座舱等级", width=100, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.flight = []
        self.date = []
        self.useracc = []
        self.cabin = []

        self.get_ticket()

        self.var_flight = StringVar()
        self.var_date = StringVar()
        self.var_useracc = StringVar()
        self.var_cabin = StringVar()

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置

        # 机场代号
        self.left_top_1_label = Label(self.frame_left_top, text="航班号：", font=('宋体', 15))
        self.left_top_1_entry = Entry(self.frame_left_top, textvariable=self.var_flight, font=('宋体', 15))
        self.left_top_1_label.grid(row=1, column=0)  # 位置设置
        self.left_top_1_entry.grid(row=1, column=1)
        # 所在城市
        self.left_top_2_label = Label(self.frame_left_top, text="日期：", font=('宋体', 15))
        self.left_top_2_entry = Entry(self.frame_left_top, textvariable=self.var_date, font=('宋体', 15))
        self.left_top_2_label.grid(row=2, column=0)  # 位置设置
        self.left_top_2_entry.grid(row=2, column=1)
        # 机场名称
        self.left_top_3_label = Label(self.frame_left_top, text="用户名：", font=('宋体', 15))
        self.left_top_3_entry = Entry(self.frame_left_top, textvariable=self.var_useracc, font=('宋体', 15))
        self.left_top_3_label.grid(row=3, column=0)  # 位置设置
        self.left_top_3_entry.grid(row=3, column=1)
        # 所在位置
        self.left_top_4_label = Label(self.frame_left_top, text="座舱等级：", font=('宋体', 15))
        self.left_top_4_entry = Entry(self.frame_left_top, textvariable=self.var_cabin, font=('宋体', 15))
        self.left_top_4_label.grid(row=4, column=0)  # 位置设置
        self.left_top_4_entry.grid(row=4, column=1)

        # 右上区域设置
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('宋体', 20))
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='升舱', width=20, command=lambda :
        self.update_ticket())
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='返回', width=20, command=self.back)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=5)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=5)
        self.right_top_button3.grid(row=2, column=1, padx=20, pady=5)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=5)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)

        self.frame_left_top.tkraise()
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def update_ticket(self) :
        if self.var_flight.get() == None :
            messagebox.showinfo('警告！', '请选择退票')
        else :
            db = pymysql.connect(host="localhost",
                                 user="root",
                                 password="sam20001207",
                                 database="air_ms")
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            # SQL 语句
            print()
            sql0 = "SELECT purchase_cabin FROM user_purchase_info WHERE user_account = '%s' and flight_id = '%s'" \
                   "and flight_date = '%s'" % (self.var_useracc.get(), self.var_flight.get(), self.var_date.get())
            print(self.var_useracc.get(), self.var_flight.get(), self.var_date.get())
            sql1 = "DELETE FROM user_purchase_info WHERE user_account = '%s' and flight_id = '%s'" \
                   "and flight_date = '%s'" % (self.var_useracc.get(), self.var_flight.get(), self.var_date.get())

            try :
                cursor.execute(sql0)  # 执行sql语句
                results = cursor.fetchall()
                print(results)
                for row in results :
                    cabin = row[0]
                print("sql0")
                print(cabin)
                cursor.execute(sql1)  # 执行sql语句
                print("sql1")
                if cabin == 'Y 经济舱' :
                    sql2 = "UPDATE standby_ticket_info set yt_left = yt_left + 1 " \
                           "WHERE flight_id = '%s' and flight_date = '%s'" % (
                           self.var_flight.get(), self.var_date.get())
                elif cabin == 'C 商务舱' :
                    sql2 = "UPDATE standby_ticket_info set ct_left = ft_left + 1 " \
                           "WHERE flight_id = '%s' and flight_date = '%s'" % (
                           self.var_flight.get(), self.var_date.get())
                else :
                    sql2 = "UPDATE standby_ticket_info set ft_left = ft_left + 1 " \
                           "WHERE flight_id = '%s' and flight_date = '%s'" % (
                           self.var_flight.get(), self.var_date.get())
                cursor.execute(sql2)
                print("sql2")
                print(self.var_cabin.get())
                if self.var_cabin.get() == 'Y 经济舱' :
                    buynum = 3
                elif self.var_cabin.get() == 'F 头等舱' :
                    buynum = 1
                else :
                    buynum = 2
                sql3 = "call buy_tick('%s', '%s', '%s', %d, @ret);" % \
                       (self.var_flight.get(), self.var_date.get(), self.var_useracc.get(), buynum)
                sql4 = "select  @ret"
                re_s = ''
                try :
                    cursor.execute(sql3)  # 执行sql语句
                    cursor.execute(sql4)  # 查询调用存储过程后返回的参数
                    for result in cursor.fetchall() :
                        re_s = result[0]
                except :
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('错误！', '购买错误！')
                if re_s == 'True' :
                    if buynum == 1 :
                        messagebox.showinfo('成功！', '头等舱升舱成功！')
                    if buynum == 2 :
                        messagebox.showinfo('成功！', '商务舱升舱成功！')
                    if buynum == 3 :
                        messagebox.showinfo('成功！', '经济舱 成功！')
                else :
                    messagebox.showinfo('错误！', '失败！')
                db.commit()  # 提交到数据库执行
            except :
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

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
        self.var_useracc.set(self.row_info[2])
        self.var_cabin.set(self.row_info[3])
        print('1')

    def get_ticket(self) :
        self.delButton(self.tree)
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        # SQL 语句
        sql = "select flight_id, flight_date, user_account, purchase_cabin from user_purchase_info;"
        try :
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            print(1)
            for row in results :
                self.flight.append(row[0])
                self.date.append(row[1])
                self.useracc.append(row[2])
                self.cabin.append(row[3])
            db.close()
        except :
            db.rollback()  # 发生错误时回滚
            messagebox.showinfo('错误！', '出错了！')
        for i in range(len(self.flight)) :  # 写入数据
            self.tree.insert('', i, values=(self.flight[i], self.date[i], self.useracc[i], self.cabin[i]))

        for col in self.columns :  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col : self.tree_sort_column(self.tree, _col, False))

    def tree_sort_column(self, tv, col, reverse) :  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l) :  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda : self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def back(self) :
        AdminMainPage(self.window)  # 显示主窗口 销毁本窗口


# 管理员航班操作界面
class AdminAirportPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = Tk()  # 初始框的声明
        self.window.title('管理员航班操作界面')

        self.frame_left_top = tk.Frame(width=1024, height=200)
        self.frame_right_top = tk.Frame(width=200, height=200)
        self.frame_center = tk.Frame(width=600, height=400)
        self.frame_bottom = tk.Frame(width=650, height=50)

        # 定义下方中心列表区域
        self.columns = ("机场代号", "机场名称", "所在城市", "地理位置")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("机场代号", width=70, anchor='center')  # 表示列,不显示
        self.tree.column("所在城市", width=70, anchor='center')
        self.tree.column("机场名称", width=200, anchor='center')
        self.tree.column("地理位置", width=200, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.iata = []
        self.name = []
        self.city = []
        self.location = []
        # 打开数据库连接
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="sam20001207",
                             database="air_ms")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM city_airport_info"  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.iata.append(row[0])
                self.city.append(row[1])
                self.name.append(row[2])
                self.location.append(row[3])

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.iata), len(self.name), len(self.city), len(self.location))):  # 写入数据
            self.tree.insert('', i, values=(self.iata[i], self.city[i], self.name[i], self.location[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="机场信息:", font=('宋体', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_iata = StringVar()  # 声明学号
        self.var_name = StringVar()  # 声明姓名
        self.var_city = StringVar()  # 声明性别
        self.var_location = StringVar()  # 声明年龄
        # 机场代号
        self.right_top_id_label = Label(self.frame_left_top, text="机场代号：", font=('宋体', 15))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_iata, font=('宋体', 15))
        self.right_top_id_label.grid(row=1, column=0)  # 位置设置
        self.right_top_id_entry.grid(row=1, column=1)
        # 所在城市
        self.right_top_city_label = Label(self.frame_left_top, text="所在城市：", font=('宋体', 15))
        self.right_top_city_entry = Entry(self.frame_left_top, textvariable=self.var_city, font=('宋体', 15))
        self.right_top_city_label.grid(row=2, column=0)  # 位置设置
        self.right_top_city_entry.grid(row=2, column=1)
        # 机场名称
        self.right_top_name_label = Label(self.frame_left_top, text="机场名称：", font=('宋体', 15))
        self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('宋体', 15))
        self.right_top_name_label.grid(row=3, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=3, column=1)
        # 所在位置
        self.right_top_loc_label = Label(self.frame_left_top, text="所在位置：", font=('宋体', 15))
        self.right_top_loc_entry = Entry(self.frame_left_top, textvariable=self.var_location,font=('宋体', 15))
        self.right_top_loc_label.grid(row=4, column=0)  # 位置设置
        self.right_top_loc_entry.grid(row=4, column=1)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('宋体', 20))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建信息',  width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='删除信息',  width=20, command=self.del_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='返回', width=20, command=self.back)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        AdminMainPage(self.window)  # 显示主窗口 销毁本窗口

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_iata.set(self.row_info[0])
        self.var_city.set(self.row_info[1])
        self.var_name.set(self.row_info[2])
        self.var_location.set(self.row_info[3])
        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_iata,
                                        font=('宋体', 15))
        print('')

    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def new_row(self):
        print('123')
        print(self.var_iata.get())
        print(self.iata)
        if str(self.var_iata.get()) in self.iata:
            messagebox.showinfo('警告！', '该机场已存在！')
        else:
            if self.var_iata.get() != '' and self.var_name.get() != '' and self.var_city.get() != '' and self.var_location.get() != '':
                # 打开数据库连接
                db = pymysql.connect(host="localhost",
                                     user="root",
                                     password="sam20001207",
                                     database="air_ms")
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                # SQL 插入语句
                sql1 = "INSERT INTO city_airport_info VALUES ('%s', '%s', '%s', '%s')" % \
                        (self.var_iata.get(), self.var_city.get(), self.var_name.get(), self.var_location.get())
                try:
                    cursor.execute(sql1)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                db.close()  # 关闭数据库连接

                self.iata.append(self.var_iata.get())
                self.name.append(self.var_name.get())
                self.city.append(self.var_city.get())
                self.location.append(self.var_location.get())
                index_num = len(self.iata) - 1
                self.tree.insert('', index_num, values=(
                    self.iata[index_num], self.city[index_num], self.name[index_num], self.location[index_num]))
                self.tree.update()
                messagebox.showinfo('提示！', '机场信息新建成功！')
            else:
                messagebox.showinfo('警告！', '请填写数据')

    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = pymysql.connect(host="localhost",
                                 user="root",
                                 password="sam20001207",
                                 database="air_ms")
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "DELETE FROM city_airport_info WHERE airport_iata = '%s'" % (self.row_info[0])  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            id_index = self.iata.index(self.row_info[0])
            print(id_index)
            del self.iata[id_index]
            del self.name[id_index]
            del self.city[id_index]
            del self.location[id_index]
            print(self.iata)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())


if __name__ == '__main__':
    window = tk.Tk()
    AdminMainPage(window)