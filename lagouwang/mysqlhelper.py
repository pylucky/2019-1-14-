import pymysql

# 创建mysql相关的类
class MysqlHelper(object):
    # 初始化函数, 实例化的时候自动执行
    def __init__(self):
        # 连接mysql的代码
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',database='cc', charset='utf8')
        # 创建游标, 目的是为了执行sql语句
        self.cursor = self.db.cursor()

    # 这个函数是我们会反复调用的函数, 目的是执行sql语句, sql是要执行的语句, data是需要插入的数据
    def execute_modify_sql(self, sql, data=None):
        # 执行
        self.cursor.execute(sql, data)
        # 数据库的提交
        self.db.commit()
    # 析构函数, 本个对象再也没有人使用以后, 这个函数自动执行
    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.db.close()

if __name__ == '__main__':
    sql = 'insert into xici(title,ip) VALUES (%s,%s)'
    data = ('没人敢睡觉','2',)
    myhelper = MysqlHelper()
    myhelper.execute_modify_sql(sql, data)

    print('Mysql连接成功')