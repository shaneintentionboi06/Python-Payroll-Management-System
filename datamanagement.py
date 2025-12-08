#Errors
class noinput(Exception):
    pass
class fetcher:
    def __init__(self,cursor):
        self.cursor = cursor
        self._columns_ = self._fetchtablesturcture_()
        
    def addemp(self,Num): pass
    
    def viewdata(self,sview=None,Columns=None):
        '''
        Docstring for viewdata
        
        :param self: Used to access cursor
        :param sview: a special attribute that starts specified views (string)
        :param Columns: a tuple of tuples like (("Attendence","Attend_ID"),("Employee","Name").......) Ignored If sview provided
        '''
        if sview:
            self.cursor.execute(f"select * from {sview}")
        elif Columns:
            #First Get the Header
            self.cursor.execute(f"select {Columns}  from Everything")
        else:
            raise noinput("No Value Provided")
            
        
    def updatedata(self,ID,table,entries): #to keep moving I need to decide a UI or not for now I'LL get 
        '''This Functions updates a record'''
        self.cursor.execute(f"update {table} set {entries} where Employee_ID = {ID}")
        
    def deleteentity(self,table,ID): 
        self.cursor.execute(f"delete from {table} where Employee_ID= {ID}")
    def deletepayroll(self,PayID):
        self.cursor.execute(f"delete from Payroll where Payroll_ID = {PayID}")

    def empdata(self,name,field): 
        pass
    
    def empdata(self,empname): pass
    
    
    def fireemp(self,Name): pass
    
    def Salupdate(self,Name,Salary): pass
    
    def exportempdata(self, Name, Salary): pass
    
    def Attend(self,Name): pass
    
    def pay(self, employee): pass

    def paymentdetails(self,Name): pass
    
        
    def _fetchtablesturcture_(self):
        names = self.cursor.execute("select name from sqlite_master where type='table'").fetchall()
        Columns = {}
        for table in names:
            self.cursor.execute(f"PRAGMA table_info({table[0]});")
            Columns[table[0]] = set()
            for row in self.cursor:
                Columns[table[0]].add((row[1],row[2]))
                
        return Columns

if __name__ == "__main__":
    import dbtransit
    DB = dbtransit.Connection("database.db")
    Feteher = fetcher(DB.get_cursor())
    print(Feteher._columns_)
    # print(Feteher.printtable('Attendence'))