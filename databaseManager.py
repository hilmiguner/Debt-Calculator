from sqlite3 import connect

class DBManager:
    def __init__(self):
        try:
            self.connection = connect(database="Data/debtDB.db")
            self.cursor = self.connection.cursor()
            print("Connection established.")
        except Exception as err:
            print(err)

    def __del__(self):
        try:
            self.connection.close()
            print("Connection disconnected.")
        except Exception as err:
            print(err)

    def addRow(self, name: str, debt: float, date: str):
        sql = f"INSERT INTO debtUser1toUser2 VALUES ({name},{debt},{date})"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as err:
            print(err)
