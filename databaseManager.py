from sqlite3 import connect
from datetime import  datetime

class DBManager:
    def __init__(self):
        try:
            self.connection = connect(database="Data/debtDB.db")
            self.cursor = self.connection.cursor()
            print(f"[{datetime.now()}] - Connection established.")
        except Exception as err:
            print(err)

    def __del__(self):
        try:
            self.connection.close()
            print(f"[{datetime.now()}] - Connection disconnected.")
        except Exception as err:
            print(err)

    def addRow(self, tableName: str, name: str, debt: float, date: str):
        sql = f"INSERT INTO {tableName} VALUES ('{name}','{debt}','{date}')"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as err:
            print(err)

    def getRows(self, tableName: str, columns=None):
        if columns is None:
            columns = ["Name", "Debt", "Date"]
        if len(columns) == 3:
            sql = f"SELECT * FROM {tableName}"
        else:
            sql = "SELECT " + ",".join(["{}"]*len(columns)) + f" FROM {tableName}"
            sql = sql.format(*columns)
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as err:
            print(err)
            return -1

