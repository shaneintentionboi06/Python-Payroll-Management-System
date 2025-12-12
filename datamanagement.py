from math import floor
from datetime import datetime,time,date,timedelta
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
        tablemap.pop('sqlite_sequence')
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
    
    def viewdata(self,*Columns,sview=None,table='all'):

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
                return Output
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
            # print(tables)
            
            #First Get the Header
            command = f"select {','.join(tablecalls)} from {tables}"
            # print(command)
            # self.cursor.execute(command)
            Output = [i for i in self.cursor.execute(command)]
            return [Columns] + list(Output)
        elif table != 'all':
            self.cursor.execute(f"select * from {table}") #Handling Errors in TUI
        elif table == 'all':
            alltables = {}
            for tab in self._column_map_.keys():
                data,head = [],[]
                self.cursor.execute(f"pragma table_info({tab})")
                for col in self.cursor: head.append(col[1])
                self.cursor.execute(f'select * from {tab}')
                data.append(self.cursor.fetchall())
                alltables[tab]=(tuple(head),tuple(*data))
            return alltables
        else:
            raise noinput("No Value Provided")
    def exporttempdata(self,ID): 
        import csv
        Data = []
        for table,columns in self._column_map_.items():
            if table == "Department": continue
            command = f"select {','.join(columns)} from {table} where Employee_ID = {ID}"
            self.cursor.execute(command)
            Data.append(columns)
            # row = self.cursor.fetchall()
            # rows= []
            # print(row)
            for row in self.cursor:
                Data.append(row)
            # row[0] = row[0].lstrip('(').rstrip(')').split(',')
        # print(Data)
        with open(f'Employee{ID}.csv','w') as file: 
            Writer = csv.writer(file)
            Writer.writerows(Data)
        # print("Data Exported")
    # def empdata(self,ID,Columns=None): 
    #     column_map = {"Name":"Employee",}
        
    #     return Output
    def markattendance(self,ID,Attend):
        today=date.today().strftime('%Y-%m-%d')
        Time = datetime.now()
        Out_time = Time + timedelta(hours=6)
        query = "Insert into Attendance (Employee_ID, Attendance_Date, Attendance, In_Time,Out_Time) Values (?, ?, ?, ?, ?)"
        values=(ID,today,Attend,Time.strftime('%H:%M'),Out_time.strftime('%H:%M'))
        self.cursor.execute(query,values)
        self.cursor.connection.commit()            


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

    def Calc_PF(self,B_Salary):
        return floor(B_Salary*0.12)
    def Prof_tax(self,Salary):
        if Salary > 10000:
            return 200
        elif 7500 < Salary < 10000:
            return 175
        else:
            return 0 
    def inc_Tax(self,Salary):
        taxable = Salary - 75000
        if taxable <= 300000:
            return 0
        
        if taxable > 300000:
            return floor(0.5*taxable)
        #real-life Tax Regime Varies
        
    def adddata(self,Data):
        dept_name= Data.get('Department_Name')
        self.cursor.execute("select Dept_ID from Department where Department_Name= ?",(dept_name,))
        res = self.cursor.fetchone()
        
        if res:
            dept_id = res[0]
        else:
            self.cursor.execute('insert into Department (Department_Name) values (?)',(dept_name,))
            self.cursor.execute("select Dept_ID from Department where Department_Name= ?",(dept_name,))
            res = self.cursor.fetchone()
            dept_id = res[0]
        emp_query= "Insert into Employee (Name, Date_of_Joining, Designation, Department_ID, ContactNo) values (?, ?, ?, ?, ?)"
        emp_values = (
            Data.get("Name"),
            Data.get("Date_of_Joining"),
            Data.get("Designation"),
            dept_id,
            Data.get('ContactNo')
        )
        self.cursor.execute(emp_query,emp_values)
        last_emp_id = self.cursor.lastrowid
        
        sal_query="INSERT INTO Salary (Employee_ID, Basic_Salary, HRA, DA, Other_Allowance, PF_Contribution, Pro_Tax, Inc_Tax, Other_Deductions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        sal_values = (
            last_emp_id,
            Data.get("Basic_Salary",0),
            Data.get("HRA",0),
            Data.get("DA",0),
            Data.get("Other_Allowance",0),
            self.inc_Tax(eval(Data.get("Basic_Salary"))),
            self.Prof_tax(eval(Data.get("Basic_Salary"))),
            self.inc_Tax(eval(Data.get("Basic_Salary"))),
            0
        )
        self.cursor.execute(sal_query,sal_values)
        self.cursor.connection.commit()
if __name__ == "__main__":
    import dbtransit
    DB = dbtransit.Connection("database.db")
    # DB.createdatasturcture()
    Feteher = fetcher(DB.get_cursor())
    # Feteher.exporttempdata(1)
    print(Feteher.viewdata())
    # Entries = Feteher.viewdata("Attendance","In_Time","Out_Time","Name","Employee_ID")
    # for i in Entries: print(i)
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
# class editor(fetcher):
    
#     def __init__(self, cursor):
#         super().__init__(cursor)

    
#     def Attend(self,Name): pass

#     def pay(self, employee): pass

#     def fireemp(self,Name): pass
    
#     def empdata(self,empname): pass
        
#     def Salupdate(self,Name,Salary): pass
    
#     def deleteentity(self,table,ID): 
#         self.cursor.execute(f"delete from {table} where Employee_ID= {ID}")
    
#     def deletepayroll(self,PayID):
#         self.cursor.execute(f"delete from Payroll where Payroll_ID = {PayID}")

#     def updatedata(self,ID,table,entries): #to keep moving I need to decide a UI or not for now I'LL get 
#         '''This Functions updates a record'''
#         self.cursor.execute(f"update {table} set {entries} where Employee_ID = {ID}")
    