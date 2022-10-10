from sqlite3 import connect
from datetime import datetime

class DBManager:
    def __init__(self):
        try:
            self.connection = connect(database="Data/debtDB.db")
            self.cursor = self.connection.cursor()
            print(f"[{datetime.now()}] - Database connection established.")
        except Exception as err:
            print(err)

    def __del__(self):
        try:
            self.connection.close()
            print(f"[{datetime.now()}] - Database connection disconnected.")
        except Exception as err:
            print(err)

    def addRow(self, tableName: str, name: str, debt: float, date: str):
        sql = f"INSERT INTO {tableName}(Name, Debt, Date)VALUES ('{name}','{debt}','{date}')"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as err:
            print(err)

    def getRows(self, tableName: str, columns=None):
        if columns is None:
            columns = ["ID", "Name", "Debt", "Date"]
        sql = "SELECT " + ",".join(["{}"]*len(columns)) + f" FROM {tableName}"
        sql = sql.format(*columns)
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as err:
            print(err)
            return -1

    def editRow(self, tableName: str, ID: int, newValues: list):
        sql = f"UPDATE {tableName} SET Name='{newValues[0]}', Debt={newValues[1]}, Date='{newValues[2]}' WHERE ID={ID}"
        print(sql)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as err:
            print(err)

    def deleteRow(self, tableName: str, ID: int):
        sql = f"DELETE FROM {tableName} WHERE ID={ID}"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as err:
            print(err)
