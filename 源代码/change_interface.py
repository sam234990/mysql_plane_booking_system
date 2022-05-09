import pymysql

class test():
    def __init__(self):
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
              % (self.var_dep_city, self.var_arr_city, self.var_flight_date)  # SQL 查询语句
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
        db.close()  # 关闭数据库连接


if __name__ == '__main__':
    test()