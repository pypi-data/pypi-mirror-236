import pymysql


class Mysql:
    def __init__(self, host=None, port=None, database=None, user=None, password=None, connect_timeout=20, read_timeout=20, write_timeout=20):
        self.conn = pymysql.connect(
            host=host,
            port=int(port),
            database=database,
            user=user,
            passwd=str(password),
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            write_timeout=write_timeout,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def count(self, table, where=""):
        cur = self.conn.cursor()
        sql = f"select count(1) cnt from {table}"
        if where:
            sql += f" WHERE {where}"
        cur.execute(sql)
        data = cur.fetchone()
        return data["cnt"]

    def execute(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def query(self, sql):
        cur = self.conn.cursor()

        cur.execute(sql)
        data = cur.fetchall()
        return list(data)

    def fetch(self, sql, *args, **kwargs):
        cur = self.conn.cursor()
        cur.execute(sql, *args, **kwargs)
        data = cur.fetchone()
        return data

    def update(self, table=None, data=None, where=None):
        cur = self.conn.cursor()
        set_list = [f'`{k}`="{v}"' for k, v in data.items()]
        sql = f"update {table} set {','.join(set_list)}"
        if where:
            sql += f"where {where}"
        cur.execute(sql)
        self.conn.commit()

    def insert(self, table=None, data_list: list = []):
        cur = self.conn.cursor()
        for data in data_list:
            field = ",".join([f"`{key}`" for key in data.keys()])
            value = ",".join([f'"{val}"' for val in data.values()])
            sql = f"insert into {table}({field}) values({value})"
            cur.execute(sql)
        self.conn.commit()

    def quit(self):
        self.conn.close()