from math import floor
from datetime import datetime,time,date,timedelta
from sqlite3 import InterfaceError
#Errors
class noinput(Exception):
    pass
class Fetcher:
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
        self.cursor.execute(f"select Employee_ID from Employee where Employee_ID = {ID}")
        if self.cursor.fetchone():
            for table,columns in self._column_map_.items():
                if table == "Department": continue
                command = f"select {','.join(columns)} from {table} where Employee_ID = {ID}"
                self.cursor.execute(command)
                Data.append(tuple(columns))
                # row = self.cursor.fetchall()
                # rows= []
                # print(row)
                for row in self.cursor:
                    Data.append(row)
                # row[0] = row[0].lstrip('(').rstrip(')').split(',')
            print(Data)
            if len(Data) == 0: raise noinput("Employee Not Found")    
            else:
                with open(f'Employee{ID}.csv','w') as file: 
                    Writer = csv.writer(file)
                    Writer.writerows(Data)
        else:
            raise noinput("The given ID is not Valid")
        
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
        try:
            self.cursor.execute("select Employee_ID from Employee")
            self.cursor.execute(query,values)
        except InterfaceError as err:
            raise noinput('Invalid or No Input Provided')
        else: self.cursor.connection.commit()            


    def paymentdetails(self,ID): 
        self.cursor.execute(f"select MAX(Salary_ID) from Salary where Employee_ID = {ID}")
        Salary_ID = self.cursor.fetchone()
        self.cursor.execute(f'select * from Salary where Salary_ID = {Salary_ID[0]} ;')
        Details = self.cursor.fetchone()
        return Details
    
        
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
            self.inc_Tax(int(Data.get("Basic_Salary"))),
            self.Prof_tax(int(Data.get("Basic_Salary"))),
            self.inc_Tax(int(Data.get("Basic_Salary"))),
            0
        )
        self.cursor.execute(sal_query,sal_values)
        self.cursor.connection.commit()
    def updatedata(self,upcolumn,value,ID): 
        table = None
        for name,columns in self._column_map_.items():
            if upcolumn in columns : table = name
        self.cursor.execute(f'Update {table} set {upcolumn} = {value} where Employee_ID = {ID}')
        self.cursor.connection.commit()  
if __name__ == "__main__":
    import dbtransit
    DB = dbtransit.Connection("database.db")
    # DB.createdatasturcture()
    Feteher = fetcher(DB.get_cursor())
    # Feteher.exporttempdata(2000)
    Feteher.paymentdetails(2)
    # Feteher.updatedata(upcolumn='Department_ID',value=7,ID=1)
    