Database Sturcture -
Table       Columns
Employee    Employee_ID(Integer), Name(VARCHAR(100)), Date_of_joining(DATE), Designation(VARCHAR(50)), Department(VARCHAR(100)),ContactNo(Varchar(15))

Salary      Salary_ID(Integer), Employee_ID(Integer,Foreign), Basic_Salary(Int),  HRA(Int), DA(Int), Other_Allowance(Int), PF_Contributions(Int), Pro_Tax(Int), Inc_Tax(Int), Other_Deductions(Int) 

Payroll     Payroll_ID(Integer), Employee_ID(Integer,Foreign), Pay_Period_Days(Int), Gross_Salary(Int), Net_Salary(Int), Deductions(Int), Bonuses_Added(Int), Date_of_payment(Date)

Attendence  Attend_ID(Int), Employee_ID(Integer,Foreign), Date(Date), In-Time(Time), Out-Time(Time)

Department  Dept_ID(Integer),Dept_Name

Storing money as integer as we don't have decimal in sqlite

Goals - 
    1. Implement the Database (Done)
    2. Make Existing Code work with sqlite rather than Mysql (Not doing this)
    3. Need to create Views to look across different tables
        1. Everything(Every Column) 2. Attendance(Name with Attendace) 3.Payment(Name with payment history) 4. Department(Employees in a Department)


New Idea - Snapshots to recover the database