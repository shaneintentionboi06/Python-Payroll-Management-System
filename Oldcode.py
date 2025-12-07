#Main Payroll Program (My class 12th Project, this project went well back then)
import mysql as msq
import datetime
mydb = msq.connect(host= "localhost" , user= "root" , passwd= "Mech@paul123" , database = "company")
if mydb.is_connected(   ):         #ConnectionTest
    print('Database Connected')
    Cur= mydb.cursor()
    def printdata():
        try:
            Cur.execute("show tables")
            X = Cur.fetchall()
            print('Which tables? Select a Number')
            TableNames = []
            for i in range(len(X)):
                Y=X[i][0]
                TableNames.append(Y)
                print(i,Y)
            VNO=[i for i in range(len(TableNames))]
            Z = input("Enter ")
            if Z.isnumeric and int(Z) in VNO :
                Table = TableNames[int(Z)]
                Cur.execute(f"desc {Table}")
                Desc=[row[0] for row in Cur.fetchall()]
                print(Desc)
                if "Status" in Desc:
                    Desc.remove("Status")
                
                Query = f" select {', '.join(Desc)} from "
                Cur.execute(Query+Table)
                Data = Cur.fetchall()
                if len(Data) == 0:
                    print("No Records")
                else:
                    for i in Data:
                        print(i)
            else :
                print('that is not in range')
        except msq.Error as err:
            print("Error: ", err)

    def MEmp():
        def Replace(list,old,new):
            X=list.index(old)
            list[X]= new
        # Fetch column names for both tables
        try:
            Cur.execute("DESC employee")
            employee_fields = [row[0] for row in Cur.fetchall()][1:]
            Cur.execute("DESC salary_structure")
            salary_fields = [row[0] for row in Cur.fetchall()][1:]
            employee_fields.remove('Status')

            NO = int(input("Enter No of Employees to add: "))
            
            last_salary_id = ''
            #Entering Employee Data
            for j in range(NO):
                employee_data = []
                Manydata = []
                SManydata = []
                for field in employee_fields:
                    if field == 'Salary_ID':
                    # Add the Salary_ID to the employee data later 
                        X='SID_Placeholder'
                        employee_data.append(X)
                        continue
                    elif field == "Date_of_joining" : 
                        X = datetime.date.today()
                        employee_data.append(X)
                    elif field == "Authority" : 
                        X = ""
                        while True:
                            X = input("Enter Admin or Employee")
                            if X == "Admin" or X == "Employee":
                                employee_data.append(X)
                                break
                            else:
                                print("Only input Admin Or Employee" )
                        continue
                    elif field == "Status":
                        continue
                    else:
                        X = input(f"Enter {field}: ")
                        if X== '':
                            X = 0
                            employee_data.append(X)
                        else:
                            employee_data.append(int(X) if str(X).isnumeric() else X)
                salary_data = []
                for field in salary_fields:
                    X = input(f"Enter {field}: ")
                    salary_data.append(int(X) if X.isnumeric() else X)
    
                # Insert into salary_structure table; Salary_ID will be auto-incremented
                insert_salary_query = f"INSERT INTO salary_structure ({', '.join(salary_fields)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                SManydata.append(tuple(salary_data))
                Cur.executemany(insert_salary_query, SManydata)
                mydb.commit()
                #fetching Salary Id
                # Assuming the last inserted Salary_ID is the one to use
                Cur.execute('select Salary_ST_ID from salary_structure')
                Data = Cur.fetchall()
                last_salary_id = Data[len(Data)-1][0]
                Replace(employee_data,'SID_Placeholder',last_salary_id)
                Manydata.append(tuple(employee_data))

                # Now, insert into employee table
                insert_employee_query = f"INSERT INTO employee ({', '.join(employee_fields)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                Cur.executemany(insert_employee_query, Manydata)
                mydb.commit()
                print(f"{len(Manydata)} employees added successfully.")
        except msq.Error as err:
            print("Error :",err)
        finally:
            mydb.commit()

    def empdel():
        try:
            Cur.execute("desc employee")
            Desc = Cur.fetchall()
            COM = "select "+str(Desc[0][0])+","+str(Desc[1][0])+" from employee where Status= 'Active' "
            Cur.execute(COM)
            Data = Cur.fetchall()
            for i in Data:
                print(i)
            MES= "Enter "+str(Desc[0][0])+" to delete"
            X= int(input(MES))
            Sql = 'UPDATE employee SET Status = "Fired" WHERE Employee_ID = %s'
            val = (X,)
            Cur.execute(Sql,val)
            mydb.commit()
            print(Cur.rowcount, "details deleted")
        except msq.Error as err:
            print("Error :",err)
        finally:
            mydb.commit()
    def empupdate():
        try:
            Cur.execute("desc employee")
            Desc = Cur.fetchall()
            Fields=[]
            for i in Desc:
                Fields.append(i[0])
            Cur.execute("select * from employee")
            Data = Cur.fetchall()
            print(Fields)
            for i in Data:
                print(i)
            I = int(input("Enter ID of Employee"))
            X=input("whcih Field to change")
            if X in Fields:
                F= input("Enter New Value")
                Update = f"UPDATE employee SET {X} = %s WHERE Employee_ID = %s"
                Cur.execute(Update,(F,I))
                mydb.commit()
                print(Cur.rowcount, "details Updated")
            else:
                print("No Such Field")
        except msq.Error as err:
            print(f"Error: {err}")

        finally:
            print("Done")

    def salupdate():
        try:
            Cur.execute("desc salary_structure")
            Desc = Cur.fetchall()
            Fields=[]
            for i in Desc: Fields.append(i[0])
            Cur.execute("select * from salary_structure")
            Data = Cur.fetchall()
            print(Fields)
            for i in Data:
                Cur.execute(f"select Name from employee where Salary_ID = {i[0]}")
                Name = Cur.fetchall()
                print(i,Name)
            I = int(input("Enter ID of salary_structure"))
            X=input("whcih Field to change")
            if X in Fields:
                F= input("Enter New Value")
                Update = f"UPDATE salary_structure SET {X} = %s WHERE Salary_ST_ID = %s"
                Cur.execute(Update,(F,I))
                mydb.commit()
                print(Cur.rowcount, "details Updated")
            else:
                print("No Such Field")
        except msq.Error as err:
            print(f"Error: {err}")

        finally:
            print("Done")
            
    def Empexport():
        import csv
        file=open('Payroll_data.csv','w')
        Write=csv.writer(file)
        Cur.execute("select * from employee")
        Data = Cur.fetchall()
        for i in Data:
            file.write(str(i)+"\n")
        file.close()
        print("File Exported")
    
    def Attend():
        try:
                Cur.execute("desc employee")
                DA = Cur.fetchall()
                fields = [r[0] for r in DA ]
                retquery= "select " + str(fields[0]) + "," + str(fields[1]) + " from employee"
                Cur.execute(retquery)
                EmpData = Cur.fetchall()
                print(EmpData)
                ID = input("Enter your employee_ID")
                Cur.execute('desc attendance')
                Ad = Cur.fetchall()
                ATfields=[r[0] for r in Ad]
                Rec = []
                for field in ATfields:
                        if field == "Attend_ID":
                                continue
                        elif field == "Date":
                                X= datetime.date.today()
                                Rec.append(X)
                        elif field== "Present_Absent":
                                X= "Present"
                                Rec.append(X)
                        elif field == "Employee_ID":
                                X=ID
                                Rec.append(X)
                        else:
                                X= input(f"Enter {field}: ")
                                if X== '':
                                        X = 0
                                        Rec.append(X)
                                else:
                                        Rec.append(int(X) if str(X).isnumeric() else X)
                Data=(tuple(Rec))
                ATfields.remove("Attend_ID")
                insert_attend_query = f"INSERT INTO attendance ({', '.join(ATfields)}) VALUES (%s, %s, %s, %s)"
                Cur.execute(insert_attend_query,Data)
                mydb.commit()
        except msq.Error as err:
                print("Error :",err)
        finally:
                print("Attendance Marked")          
    
    def pay():
                try:
                    Cur.execute("desc employee")
                    DA = Cur.fetchall()
                    fields = [r[0] for r in DA ]
                    retquery= "select " + str(fields[0]) + "," + str(fields[1]) + " from employee where Status ='Active' "
                    Cur.execute(retquery)
                    EmpData = Cur.fetchall()
                    print(EmpData)
                    ID = input("Enter your employee_ID")
                    Cur.execute(f"select Salary_ID from employee where Employee_ID ={ID} ")
                    SALID = Cur.fetchone()
                    if SALID == None:
                        print("INVALID EMP ID")
                    else:
                        Cur.execute(f"select * from salary_structure where Salary_ST_ID = {SALID[0]}")
                        SalData = Cur.fetchone()
                        Cur.execute('desc payroll')
                        Pd = Cur.fetchall()
                        PTfields=[r[0] for r in Pd]
                        Rec = []
                        for field in PTfields:
                            if field == "Payroll_ID":
                                continue
                            elif field == "Date":
                                    X= datetime.date.today()
                                    Rec.append(X)
                            elif field== "Gross_Salary":
                                X= SalData[1]
                                Rec.append(X)
                            elif field == "Net_Salary":
                                Bon = SalData[2]+SalData[3]+SalData[4]
                                Dec = SalData[5]+SalData[7]+SalData[6]+SalData[8]
                                X=SalData[1] - Dec + Bon
                                Rec.append(X)
                            elif field == "Employee_ID" :
                                X=ID
                                Rec.append(X)
                            elif field == "Deductions":
                                X=SalData[5]+SalData[7]+SalData[6]+SalData[8]
                                Rec.append(X)
                            elif field == "Bonuses_Added":
                                X=SalData[2]+SalData[3]+SalData[4]
                                Rec.append(X)
                            elif field == "Date":
                                X=datetime.date.today()
                                Rec.append(X)
                            else:
                                X= input(f"Enter {field}: ")
                                if X== '':
                                    X = 0
                                    Rec.append(X)
                                else:
                                    Rec.append(int(X) if str(X).isnumeric() else X)
                        Data=(tuple(Rec))
                        PTfields.remove("Payroll_ID")
                        insert_attend_query = f"INSERT INTO payroll ({', '.join(PTfields)}) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        Cur.execute(insert_attend_query,Data)
                        mydb.commit()
                except msq.Error as err:
                    print("Error :",err)
                finally:
                    print("Done")          
                    
    def Paydet():
        try:
            import csv
            Cur.execute("select * from employee" )
            EMP_list=Cur.fetchall()
            for i in EMP_list:
                print(i)
            Emp_ID=input("Enter Employee_ID")
            Cur.execute(f"select * from payroll where Employee_ID = {Emp_ID}")
            PayData = Cur.fetchall()
            if PayData == None:
                print("INVALID EMP ID")
            else:
                Cur.execute(f"select Name from Employee where Employee_ID = {Emp_ID}")
                Emp_Name= Cur.fetchone()
                Cur.execute("desc payroll")
                Raw=Cur.fetchall()
                Desc = [row[0] for row in Raw] 
                Emp_data = [row for row in PayData]
                file = open(f"{Emp_Name[0]} Payment Details {datetime.date.today()}_.csv","w")
            Wr=csv.writer(file)
            Wr.writerow(Desc)
            Wr.writerows(Emp_data)
            file.close()
        except msq.Error as err:
            print("Error :",err)
        finally:
            print("Done")
        
    while True:
        print("1.Print All Data")
        print("2.New Employees")
        print("3.fire Employee")
        print("4.Update Employee Data")
        print("5.Update Salary Data")
        print("6.Export Employee Data")
        print("7.Enter Attendance")
        print("8.Make A Payment")
        print("9.Payment details View/Export") 
        print("10.Exit")

        Choice=int(input("Enter Your Choice"))
        if Choice == 1:
            printdata()
        if Choice == 2:
            MEmp()
        if Choice == 3:
            empdel()
        if Choice == 4:
            empupdate()
        if Choice == 5:
            salupdate()
        if Choice == 6:
            Empexport()
        if Choice == 7:
            Attend()
        if Choice == 8:
            pay()
        if Choice == 9:
            Paydet()
        if Choice == 10:
            print("Thank You")
            break
else:
    print("Can't access database")