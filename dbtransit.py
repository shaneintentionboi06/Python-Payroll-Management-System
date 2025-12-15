import sqlite3
import os
import DummyData
class Connection:
    '''
    Connects Database
    
    Args - 
    Database - Name of the Database file(str)
    '''
    def __init__(self,Database="database.db"):
        self.databasename = Database
        self._database_ = self.set_Database(Database)
        self._cursor_ = self.set_cursor() 
        # self.enteries = self.getrows
    def set_Database(self,db):
        database = None
        if os.path.isfile(db):
            database = sqlite3.connect(db)
            print("Connection Successful")
        else:
            Choice = input(f"The file {db} doesn't exist. Create new file?(Y/n): ")
            if Choice == "Y": 
                database = sqlite3.connect(db)
                print("File Created. Building Data Structure")
                self._createdatastructure_(database)
                dumchoice = input('Do you Want to insert some DummyData (Y/n)')
                if dumchoice == 'Y': DummyData.Insert_dummy_data()
                print("Connection Successful")
            if Choice == "n": 
                print("Connection Failed")
                quit()
        return database

    def set_cursor(self):
        return self._database_.cursor()
    def get_cursor(self):
        return self._cursor_
    def _createdatastructure_(self,database):
        '''
        Creates the sturcture(tables) of the database
        
        :param self: Description
        '''
        Cursor = database.cursor()
        tables = {"Department":"""
                Dept_ID INTEGER Primary Key autoincrement,
                Department_Name TEXT""",
                
                "Employee": """ 
                Employee_ID INTEGER Primary key autoincrement,
                Name Text,
                Date_of_Joining DATE,
                Designation Text,
                Department_ID INTEGER,
                ContactNo TEXT,
                Foreign key (Department_ID) references Department (Dept_ID) """, 
                
                "Salary":"""
                Salary_ID INTEGER Primary key,
                Employee_ID INTEGER,
                Basic_Salary INTEGER,
                HRA INTEGER,
                DA INTEGER,
                Other_Allowance INTEGER,
                PF_Contribution INTEGER,
                Pro_Tax INTEGER,
                Inc_Tax INTEGER,
                Other_Deductions INTEGER,
                Foreign key (Employee_ID) references Employee (Employee_ID) """,
                
                "Payroll": """
                Payroll_ID INTEGER Primary Key,
                Employee_ID INTEGER,
                Pay_Period_Days INTEGER,
                Gross_Salary INTEGER,
                Net_Salary INTEGER,
                Deductions INTEGER,
                Bonuses_Added INTEGER,
                Date_of_Payment DATE,
                Foreign Key (Employee_ID) references Employee (Employee_ID)
                """, 
                
                "Attendance":"""
                Attendance_ID INTEGER primary key,
                Employee_ID Integer,
                Attendance_Date Date,
                Attendance Text Check(Attendance in ('Present','Absent')),
                In_Time time,
                Out_Time time, 
                Foreign Key (Employee_ID) references Employee (Employee_ID)"""}
        views = {"Attendanceview": '''
                    select * Employee from Employee E
                    left join Department D on E.Department_ID = D.Dept_ID
                    left join Salary S on E.Employee_ID = S.Employee_ID
                    left join Payroll P on E.Employee_ID = P.Employee_ID
                    left join Attendance A on E.Employee_ID = A.Employee_ID
                 '''}
        for i,j in tables.items():
            try:
                Cursor.execute(f"Create Table {i} ({j});")
            except sqlite3.OperationalError as err:
                print(f"Error: {err}")
        print("Tables are created")
        # for i,j in views.items():
        #     try:
        #         self._cursor_.execute(f"Create view {i} as {j};")
        #     except sqlite3.OperationalError as err:
        #         print(f"Error: {err}")
        # print("Views are created(Hopeffully)")    
        database.commit()
        print("Default Data structure created")
        
        
    @staticmethod
    def checkdbs():
        """
        This functions checks for databases(.db) in the directory
        
        :return: sequence of names of all databases in the directory
        :rtype: list
        """
        directory = os.listdir()
        db = []
        for i in directory:
            if i.endswith(".db"): db.append(i)
        return db



#Testing
if __name__ == "__main__":
    from data_management import Fetcher
    print(Connection.checkdbs())
    Dataconnect = Connection("database21.db")
    Dataconnect._createdatastructure_(Dataconnect)
    Hawk = Fetcher(Dataconnect.get_cursor())
    # Hawk.cursor.execute("select name,type from sqlite_master")
    # for i in Hawk.cursor: print(i)
    Hawk.viewdata("Employee_ID")
    