import sqlite3
def Insert_dummy_data():
    """
    Inserts dummy data into the created tables.

    Args:
        host: Hostname of the MySQL server.
        user: Username to connect to the MySQL server.
        password: Password for the MySQL user.
    """
    try:
        mydb = sqlite3.connect("database.db")
        mycursor = mydb.cursor()
        #Insert Dummy Data to Department
        departments = [
            (1,"IT"),
            (2,"BS")
        ]
        sql = "INSERT INTO Department (Dept_ID,Department_Name) VALUES (?, ?)"
        # Insert dummy data into Employee
        employee_data = [
            ('John Doe', '2023-01-01', 'Manager', 1, '1234567890'),
            ('John Jacob', '2024-02-01', 'Senior Manager', 2, '1234567890'),
            ('John Jacob', '2024-02-01', 'Senior Manager', 2, '1234567890'),
            ('Shreyansh', '2025-02-01', 'CEO', 2, '8390129381'),
            ('John Who', '2024-02-01', 'Senior Manager', 2, '1234567890'),
            ('John Cena', '2024-02-01', 'Senior Manager', 2, '1234567890'),
            ('Vishesh', '2024-02-01', 'Senior Manager', 2, '1234567890'),
            ('Krishna', '2024-02-01', 'Senior Manager', 2, '1234567890'),
            ('Jane Smith', '2023-02-15', 'Engineer', 1, '9876543210')
        ]
        sql = "INSERT INTO Employee (Name, Date_of_joining, Designation, Department_ID, ContactNo) VALUES (?, ?, ?, ?, ?)"
        mycursor.executemany(sql, employee_data)

        # Insert dummy data into Salary_Structure
        salary_data = [(1, 10000, 5000, 3000, 2000, 1000, 500, 200, 100), 
                      (2, 15000, 7500, 4500, 3000, 1500, 750, 300, 150),
                      (3, 15000, 7500, 4500, 3000, 1500, 750, 300, 150),
                      (4, 15000, 7500, 4500, 3000, 1500, 750, 300, 150),
                      (5, 15000, 7500, 4500, 3000, 1500, 750, 300, 150),
                      (6, 15000, 7500, 4500, 3000, 1500, 750, 300, 150),
                      (7, 15000, 7500, 4500, 3000, 1500, 750, 300, 150),
                      (8, 15000, 7500, 4500, 3000, 1500, 750, 300, 150),
                      (9, 15000, 7500, 4500, 3000, 1500, 750, 300, 150),]
        sql = "INSERT INTO Salary (Employee_ID, Basic_Salary, HRA, DA, Other_Allowance, PF_Contribution, Pro_Tax, Inc_Tax, Other_Deductions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        mycursor.executemany(sql, salary_data)
        # mycursor.execute('select Salary_ST_ID from salary_structure')
        # Data = Cur.fetchall()
        # last_salary_id = Data[len(Data)-1][0]
        # Replace(employee_data,'SID_Placeholder',last_salary_id)
        # Insert dummy data into Payroll (you'll need to calculate values based on Salary_Structure)
        payroll_data = [
            (1, 20, 25000, 22000, 3000, 0), 
            (2, 20, 35000, 31000, 4000, 0)
        ]
        sql = "INSERT INTO Payroll (Employee_ID, Pay_Period_days, Gross_Salary, Net_Salary, Deductions, Bonuses_Added) VALUES (?, ?, ?, ?, ?, ?)"
        mycursor.executemany(sql, payroll_data)

        # Insert dummy data into attendance (example)
        attendance_data = [
            (1, '2023-11-01', 'Present', '10:00',"20:00"),
            (1, '2023-11-02', 'Present', '9:30',"20:00"),
            (2, '2023-11-01', 'Present', '10:00',"20:00"),
            (2, '2023-11-02', 'Absent', '10:00',"20:00")
        ]
        sql = "INSERT INTO Attendance (Employee_ID, Attendance_Date,Attendance, In_Time, Out_Time) VALUES (?, ?, ?, ?,?)"
        mycursor.executemany(sql, attendance_data)

        sql = "INSERT INTO Department (Dept_ID, Department_Name) VALUES (?, ?)"
        department_data = [
            (1,'Information Technology'),
            (2,'Sales Team'),
            (3,'Administration Team'),
        ]
        mycursor.executemany(sql,department_data)
        
        mydb.commit()
        print("Dummy data inserted successfully.")

    except ValueError as err:
        print(f"Error inserting dummy data: {err}")