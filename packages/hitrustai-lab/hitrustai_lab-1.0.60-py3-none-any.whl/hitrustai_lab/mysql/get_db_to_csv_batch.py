import pandas as pd
import pymysql
import numpy as np
from tqdm import tqdm


class DBDownload:
    def __init__(
        self, host="192.168.10.201",
        user="test", passwd="13572468",
        db_name="diiarelease",
        port="3305",
        table="tb_fraud_detect_predict_result",
        batch_size=10000,
        file_name_csv="model_predict.csv",
        sql_time=""
    ):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.port = port
        self.table = table
        self.batch_size = batch_size
        self.file_name_csv = file_name_csv
        self.sql_time = sql_time

    def get_db_need_looptime(self, batch=100000):
        con = pymysql.connect(
            db=self.db_name,
            user=self.user,
            passwd=self.passwd,
            host=self.host,
            port=self.port
        )
        
        sql_cmd = """
        SELECT count(pk_id) FROM %s %s;
        """ % (self.table, self.sql_time)
        cursor = con.cursor()
        cursor.execute(sql_cmd)
        data = cursor.fetchone()
        con.close()
        return data[0] // batch + 1

    def run(self, sql_cmd):
        con = pymysql.connect(
            db=self.db_name,
            user=self.user,
            passwd=self.passwd,
            host=self.host,
            port=self.port
        )
        pk_id = 0
        loop_times = self.get_db_need_looptime(self.batch_size)
        for i in tqdm(range(loop_times)):
            print("pk_id:", pk_id)
            sql_time = ""
            if self.sql_time == "":
                sql_time = "where "
            else:
                sql_time = self.sql_time + "and"

            sql = """%s pk_id > %d limit %d;""" % (sql_time, pk_id, self.batch_size)
            df = pd.read_sql(sql_cmd + sql, con)
            print("df長度:", len(df))
            
            
            if pk_id == 0:
                df.to_csv(self.file_name_csv, index=False)
            else:
                df.to_csv(self.file_name_csv, mode="a", header=False, index=False)
            pk_id = list(df["pk_id"][-1:])[0]


def main():
    db_name = "diia_release"
    table = "deviceinfo"
    diia = DBDownload(
        db_name=db_name,
        user="root",
        passwd="root16313302",
        host="192.168.10.112",
        port=3305,
        table=table,
        batch_size=10000,
        file_name_csv="new_diia.csv",
        sql_time="where udid like '154637530395207*%'"
    )
    sql_cmd = """
        SELECT * FROM %s.%s
    """ % (db_name, table)
    diia.run(sql_cmd)
    print("---成功---")


if __name__ == '__main__':
    main()
