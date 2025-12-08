class fetcher:
    def __init__(self,cursor):
        self.cursor = cursor
        self._columns_ = self._fetchtablesturcture_()
    
    def viewdata(self,Columns):
        '''
        Docstring for viewdata
        
        :param self: Used access cursor
        :param Columns: a tuple of tuples like (("Attendence","Attend_ID"),("Employee","Name").......)
        '''
    
        
    def updatedata(self): #to keep moving I need to decide a UI or not for now I'LL get 
        pass
    def deleteentty(self): pass
    
    def empdata(name,field): pass
    
    def empdata(self,empname): pass
    
    def addemp(self,Num): pass
    
    def fireemp(self,Name): pass
    
    def Salupdate(self,Name,Salary): pass
    
    def exportempdata(self, Name, Salary): pass
    
    def Attend(self,Name): pass
    
    def pay(self, employee): pass

    def paymentdetails(self,Name): pass
    
        
    def _fetchtablesturcture_(self):
        names = self.cursor.execute("select name from sqlite_master").fetchall()
        Columns = {}
        for table in names:
            tabledata = self.cursor.execute(f"PRAGMA table_info({table[0]});")
            Columns[table[0]] = set()
            for col in tabledata[0,3]: Columns[table[0]].add(col)
        return Columns

if __name__ == "__main__":
    import dbtransit
    DB = dbtransit.Connection("database.db")
    Feteher = fetcher(DB.get_cursor())
    print(Feteher.cursor.execute("select Name from Employee"))
    # print(Feteher.printtable('Attendence'))