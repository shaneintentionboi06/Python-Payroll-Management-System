import sqlite3
#sqlite3 does not certain datatypes like decimal or varchar


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

Database = sqlite3.connect("database.db")
Cursor = Database.cursor()
for i,j in tables.items():
    Cursor.execute(f"Create Table {i} ({j});")
print("congratulations")
