class fetcher:
    def __init__(self,cursor):
        self.cursor = cursor
        self._columns_ = self._fetchtablesturcture_()
    def printtable(self,name,columns=None):
        query =(name,columns)
        table = self.cursor.execute("select * from ?",query).fetchall()
        return table
    def _fetchtablesturcture_(self):
        names = self.cursor.execute("select name from sqlite3_master").fetchall()
        Columns = {}
        for table in names:
            tabledata = self.cursor.execute("PRAGMA table_info(?);",(table[0]))
            Columns[table[0]] = set()
            for col in tabledata: Columns.add(col)
        return Columns

    