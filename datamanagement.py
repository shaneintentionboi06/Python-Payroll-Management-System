#Errors
class noinput(Exception):
    pass
class fetcher:
    def __init__(self,cursor):
        self.cursor = cursor
        # self._columns_ = self._fetchtablesturcture_()
        self._column_map_= self._create_column_map_()
        self._views_ = self._create_view_map_()
    def _create_column_map_(self):
        #first get names of the table 
        tablemap = {}
        self.cursor.execute("select name from sqlite_master where type='table'")
        Tables = [i[0] for i in self.cursor]
        for tb in Tables:
            columns = set()
            self.cursor.execute(f"pragma table_info({tb})")
            for column in self.cursor: columns.add(column[1])
            if tb != "Employee": columns.discard("Employee_ID")
            tablemap[tb]=columns
        return tablemap
    def get_columnmap(self):
        return self._column_map_
    def _create_view_map_(self):
        viewmap = {}
        self.cursor.execute("select name from sqlite_master where type='view'")
        views = [i[0] for i in self.cursor]
        for view in views:
            Columns = list()
            self.cursor.execute("pragma table_info({view})")
            for column in self.cursor: Columns.append(column[1]) 
            viewmap[view] = tuple(Columns)
        return viewmap
    # __column_map__= _create_column_map_()
    
    def viewdata(self,*Columns,sview=None,):

        '''
        Docstring for viewdata
        
        :param self: Used to access cursor
        :param sview: a special attribute that starts specified views (string)
        :param Columns: a tuple of tuples like (("Attendence","Attend_ID"),("Employee","Name").......) Ignored If sview provided
        '''
        if sview:
            if sview in self._views_.keys:
                head = self._views_[sview]
                self.cursor.execute(f"select * from {sview}")
                Output =  [head] + [i for i in self.cursor]
        elif Columns:
            needed_table = set()
            needed_table.add("Employee")
            tablecalls = set()
            for column in Columns:
                for j,k in self._column_map_.items() :
                    if column in k:
                        needed_table.add(j)
                        tablecalls.add(j+'.'+column)
            tables = ",".join([i for i in needed_table])
            print(tables)
            
            #First Get the Header
            command = f"select {','.join(tablecalls)} from {tables}"
            print(command)
            # self.cursor.execute(command)
            Output = [i for i in self.cursor.execute(command)]
        else:
            raise noinput("No Value Provided")
        return [Columns] + list(Output)
        

    # def empdata(self,ID,Columns=None): 
    #     column_map = {"Name":"Employee",}
        
    #     return Output
    def exportempdata(self, ID): 
        self.cursor.execute(f"select * from ")
    

    def paymentdetails(self,Name): pass
    
        
    def _fetchtablesturcture_(self):
        names = self.cursor.execute("select distinct name from sqlite_master where type='table'").fetchall()
        Columns = {}
        for table in names:
            self.cursor.execute(f"PRAGMA table_info({table[0]});")
            Columns[table[0]] = set()
            for row in self.cursor:
                Columns[table[1]].add((row[1],row[2]))
                
        return Columns

class editor:

    def __init__(self,cursor):
        self.cursor = cursor

    def addemp(self,Num): pass
    
    def Attend(self,Name): pass

    def pay(self, employee): pass

    def fireemp(self,Name): pass
    
    def empdata(self,empname): pass
        
    def Salupdate(self,Name,Salary): pass
    
    def deleteentity(self,table,ID): 
        self.cursor.execute(f"delete from {table} where Employee_ID= {ID}")
    
    def deletepayroll(self,PayID):
        self.cursor.execute(f"delete from Payroll where Payroll_ID = {PayID}")

    def updatedata(self,ID,table,entries): #to keep moving I need to decide a UI or not for now I'LL get 
        '''This Functions updates a record'''
        self.cursor.execute(f"update {table} set {entries} where Employee_ID = {ID}")
        
if __name__ == "__main__":
    import dbtransit
    DB = dbtransit.Connection("database.db")
    # DB.createdatasturcture()
    Feteher = fetcher(DB.get_cursor())
    Entries = Feteher.viewdata("Attendance","In_Time","Out_Time","Name","Employee_ID")
    for i in Entries: print(i)
    # print(Feteher._columns_)
    # print(Feteher.get_columnmap())
    # print(Feteher.printtable('Attendence'))
    
    
    #     ENTRIES = [
    # ("lane", "swimmer", "country", "time"),
    # (4, "Joseph Schooling", "Singapore", 50.39),
    # (2, "Michael Phelps", "United States", 51.14),
    # (5, "Chad le Clos", "South Africa", 51.14),
    # (6, "László Cseh", "Hungary", 51.14),
    # (3, "Li Zhuhao", "China", 51.26),
    # (8, "Mehdy Metella", "France", 51.58),
    # (7, "Tom Shields", "United States", 51.73),
    # (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    # (10, "Darren Burns", "Scotland", 51.84),]
    