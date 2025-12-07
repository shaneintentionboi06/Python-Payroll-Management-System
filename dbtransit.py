import sqlite3
import os
class Connection:
    def __init__(self,Database):
        self.name = Database
        self.cursor = self.get_connection(Database) 
        # self.enteries = self.getrows
    def get_connection(self,db):
        Cursor = None
        if os.path.isfile(db):
            Cursor = sqlite3.connect(db)
            print("Connection Successful")
        else:
            Choice = input(f"The file {db} doesn't exist. Create new file?(Y/n): ")
            if Choice == "Y": Cursor = sqlite3.connect(db)
            if Choice == "n": print("Connection Failed") 
        return Cursor
    
    def createdatasturcture(self):
        
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
                
                "Attendence":"""
                Attendence_ID INTEGER primary key,
                Employee_ID Integer,
                Attendance_Date Date,
                In_Time time,
                Out_Time time, 
                Foreign Key (Employee_ID) references Employee (Employee_ID)"""}

        for i,j in tables.items():
            self.cursor.execute(f"Create Table {i} ({j});")
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
            if i.endswith(".db"): db.append()
        return db



#Testing
if __name__ == "__main__":
    Connection.checkdbs()
    Dataconnect = Connection("hola.db")
    Dataconnect.createdatasturcture()
    Cursor = Dataconnect.cursor
    print(Cursor.execute("select * from employee").fetchone())
    
    