from textual.validation import Number,Validator
from textual.app import App,ComposeResult
from textual.widgets import Header,Footer,DataTable,Static,ListView,ListItem,Button,Select,Tabs,Tab,Label,Input,Link
from textual.containers import ScrollableContainer,Container,VerticalScroll,Grid
from itertools import cycle
from textual import on 
from textual.screen import Screen,ModalScreen
from textual.notifications import Notification,Notify
from abc import ABC,abstractmethod
from textual_datepicker import DateSelect
from datetime import date
# from textual.reactive import reactive
from pyfiglet import figlet_format

#THis is the Most of the reason I am doing this project and why I hate it at the same time

cursors = cycle(['column','row','cell','none'])

class Menu(Static):
    
    head= figlet_format("Payroll",font='3-d')
    
    def compose(self):
        yield Grid(
            Label(self.head),
            Link("contribute on Github",url='https://github.com/shaneintentionboi06/Python-Payroll-Management-System',id='github'))
        yield ListView(
            ListItem(Button("View Tables",id='table')),
            ListItem(Button("Export Employee data",id='expemployee')),
            # ListItem(Button("Update Employee data",id='update')),
            ListItem(Button("Add Employee",id='add')),
            ListItem(Button("Mark Attendance",id='attend')),
            # ListItem(Button("Remove Employee",id='remove'))
        )

    @on(Button.Pressed,'#table')
    def calltable(self):
        self.app.push_screen(Tableview())
        
    @on(Button.Pressed,'#add')
    def callemp(self):
        self.app.push_screen(Form(id='addemp'))
    @on(Button.Pressed,'#expemployee')
    def callexport(self):
        self.app.push_screen(Exportdatascreen())
    @on(Button.Pressed,"#attend")
    def callattend(self):
        self.app.push_screen(Attendscreen())    

# class Thetable(Static):
#     BINDINGS= [('c','key_c','Toggle Cursors')]
#     def compose(self):
#         yield DataTable()

#     def _on_mount(self):
#         table = self.query_one(DataTable)
#         table.add_columns(*Entries[0])
#         table.add_rows(Entries[1:])
#         table.cursor_type = next(cursors)
#         table.zebra_stripes = True

#     def key_c(self):
#         table = self.query_one(DataTable)
#         table.cursor_type = next(cursors)

    # def key_c(self):
    #     table = self.query_one(DataTable)
    #     table.cursor_type = next(cursors)

class Tableview(Screen):
    def __init__(self, name = None, id = None, classes = None):
        self.tables = self.get_tables()
        super().__init__(name, id, classes)
    BINDINGS=[('escape','btn_back','Back to Main Menu'),('c','key_c','Toggle Cursor')]
    def compose(self):
        Tables = list(self.app.fetcher._column_map_.keys())
        yield Header(show_clock=True)
        yield Tabs(*Tables)
        yield DataTable(id='Table')
        yield Footer()

    def action_btn_back(self):
        self.app.pop_screen()
    # def _on_mount(self):
    #     table = self.query_one(DataTable)
    #     table.add_columns(self.tables[1].keys())
    #     table.add_rows(self.tables[1].values())
    #     table.cursor_type = next(cursors)
    #     table.zebra_stripes = True
    def on_mount(self):pass
        # table = self.query_one(DataTable)
        # table.clear(columns=True)
    def key_c(self):
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)
    def on_tabs_tab_activated(self,event:Tabs.TabActivated):
            try:
                table = self.query_one(DataTable)
                tab = self.query_one(Tabs)
                table.clear(columns=True)
                name = event.tab.label
                tabledata = self.tables[name]
                if event.tab is None: 
                    table.visible = False
                else:
                    table.visible = True
                    # table.add_columns(self.tables[1].keys())
                    for col in tabledata[0]:
                        table.add_column(col)
                    for col in tabledata[1]:
                        table.add_row(*col) 
                    # table.add_columns(*Entries[0])
                    # table.add_rows(Entries[1:])
                    table.cursor_type = next(cursors)
                    table.zebra_stripes = True
            except Exception as err:
                self.app.notify(f"Error: {err}")
    def get_tables(self): 
        return self.app.fetcher.viewdata()

        

class Attend(Static):
    def compose(self):
        yield Label("Mark Attendance", id='title')
        yield Label("Employee_ID", id='IDlabel')
        yield Input(placeholder='Enter ID',id='ID',type='integer',validate_on='submitted')
        yield Label("Name" ,id='Namelabel')
        yield Select((line,line) for line in ['Present','Absent'])
        yield Button("Mark",variant='success',id='Submit')
        

class Exportinput(Static):
    def compose(self):
        self.title = 'Export Menu'
        yield Label(self.title, id='title')
        yield Label("Employee_ID", id='IDlabel')
        yield Input(placeholder='Enter ID',id='ID',type='integer',validate_on='submitted')
        yield Label("Name" ,id='Namelabel')

class Exportdatascreen(ModalScreen):
    BINDINGS=[('escape','btn_back','Back to Main Menu')]
    def compose(self):
        yield Exportinput(classes='Dailog')
    def action_btn_back(self):
        self.app.pop_screen()
        
    def get_employee_ID(self,ID):
        try:
            if ID == 0: 
                return "Enter ID"
            else:
                self.app.fetcher.cursor.execute(f"select Name from Employee where Employee_ID = {ID}")
                return self.app.fetcher.cursor.fetchone()
        except Exception as err:
                return None
    
    @on(Input.Submitted,'#ID')
    def handle_input(self, event: Input.Submitted):
        data = event.value
        try:
            self.app.fetcher.exporttempdata(data)
            self.app.notify(f"data Exported for Emp {data}")
        except Exception as err:
            self.app.notify(f"Failed Error: {err}",severity='error')
        self.app.pop_screen()
    @on(Input.Changed,'#ID')
    def on_input_changed(self, event: Input.Changed):
        try: 
            data = event.value
            nameinput = self.query_one('#Namelabel')
            if data:    
                if data.strip():
                    Name = self.get_employee_ID(data)[0]

                    if Name:
                        nameinput.update(f"Found: {Name}")
                    else:
                        nameinput.update(f"Not Found")
            else:
                nameinput.update('Name: ')
        except TypeError as err:
            nameinput.update(f"Invalid ID. Error: ID Not Found")
        except Exception as err:
            self.app.notify(f"Error: {err}")

class Attendscreen(ModalScreen):
    BINDINGS=[('escape','btn_back','Back to Main Menu')]
    def compose(self):
        yield Attend(classes='Dailogatt')
    def action_btn_back(self):
        self.app.pop_screen()
        
    def get_employee_ID(self,ID):
        try:
            if ID == 0: 
                return "Enter ID"
            else:
                self.app.fetcher.cursor.execute(f"select Name from Employee where Employee_ID = {ID}")
                return self.app.fetcher.cursor.fetchone()
        except Exception as err:
                return None
    
    @on(Input.Submitted,'#ID')
    def handle_input(self, event: Input.Submitted):
        data = event.value
        Remark = self.screen.query_one(Select).value
        try:
            self.app.fetcher.markattendance(data,Remark)
            self.app.notify(f"Attendance Marked for Emp {data}")
            self.app.pop_screen()
        except Exception as err:
            self.app.notify(f"Failed, Error: {err}",severity='error')
            self.app.pop_screen()
    
    @on(Button.Pressed,'#Submit')
    def handle_input(self, event: Button.Pressed):
        Emp_ID = self.query_one('#ID',Input)
        data = Emp_ID.value
        Remark = self.screen.query_one(Select).value
        try:
            self.app.fetcher.markattendance(data,Remark)
            self.app.notify(f"Attendance Marked for Emp {data}")
            self.app.pop_screen()
        except Exception as err:
            self.app.notify(f"Failed, Error: {err}",severity='error')
            self.app.pop_screen()
    
    @on(Input.Changed,'#ID')
    def on_input_changed(self, event: Input.Changed):
        try: 
            data = event.value
            nameinput = self.query_one('#Namelabel')
            if data:    
                if data.strip():
                    Name = self.get_employee_ID(data)[0]

                    if Name:
                        nameinput.update(f"Found: {Name}")
                    else:
                        nameinput.update(f"Not Found")
            else:
                nameinput.update('Name: ')
        except TypeError:
            nameinput.update("Invalid ID. Please enter Employee_ID")
        except Exception as err:
            self.app.notify(f"Error  {err} ")

class Contact(Validator):
    def validate(self, value):
        if len(value) == 10: return self.success()
        else: return self.failure()

class Form(Screen):
    BINDINGS=[('escape','btn_back','Back to Main Menu')]
    def compose(self):
        self.designation = None
        yield Header()
        yield Footer()
        with VerticalScroll(id="Data_form",classes='Data_form'):    
            yield Label("Basic Details",classes='head')
            
            yield Label('Name', id='namelabel')
            yield Input(placeholder='Enter',id='Name',classes='Alpha')
            
            yield Label("Department Details",classes='head')
            yield Label('Department Name', id='deptnamelabel')
            yield Input(placeholder='Enter',id='Department_Name',classes='Alpha')
            
            yield Label("Date of Joining",id='date_of_joininglabel')
            yield Input(date.today().strftime('%Y-%m-%d'),id='Date_of_Joining')
            
            yield Label("Designation",id='designationlabel')
            yield Input(placeholder='Enter',id='Designation', value=self.designation,classes='Alpha')

            yield Label("Contact",id='Contactlabel')
            yield Input(id='ContactNo',type="integer",validators=[Contact()],max_length=10)
            
            yield Label("Salary Details",classes='head')
            yield Label("Salary Amount",id='Salaryamtlabel')
            yield Input(id='Basic_Salary',placeholder="Enter",type='integer')
            
            yield Label('House Rent Allowance',id='HRAlabel')
            yield Input(placeholder='Enter',id='HRA',type='integer')
            
            yield Label('Dearness Allowance', id='DAlabel')
            yield Input(placeholder='Enter', id='DA',type='integer')
            
            yield Label('Other Allowance',id='OTAlabel')
            yield Input(placeholder='Enter',id='Other_allowance',type='integer')
            yield Button('Submit',id='Submit',variant='success')
    
    def action_btn_back(self):
        self.app.pop_screen()
    @on(Button.Pressed,'#Submit')
    def on_submit(self):
        import string
        contactno = self.query_one("#ContactNo",Input)
        value = contactno.value.strip()
        if len(value) < 10:
            self.app.notify("Error: No. of Digits Provided for Contact are less than 10",severity='error')
            contactno.focus()
            return None
        text_fields = self.query('.Alpha')
        specialchar = set(string.punctuation)
        for field in text_fields:
            if any(char.isdigit for char in field.value):
                self.app.notify(f'Warning: {field.id} has numbers',severity='warning')
            if any(char in specialchar for char in field.value):
                self.app.notify(f'Warning: {field.id} has special characters',severity='error')
                field.focus()
                return None
        try:
            inputs = self.query(Input) 
            form_data= {input.id:input.value for input in inputs}
            self.app.fetcher.adddata(form_data)
            self.app.notify("Employee Added")
            self.app.pop_screen()
        except SyntaxError:
            self.app.notify('Error: Invalid or required fields not provided')
        except Exception as err:
            self.app.notify(f"Error: {err}")

class Payrollmenu(Exportinput): pass

class Payrollscreen(Screen): pass
    
class Update_form(Form): pass
    

class Testrun(App):
    CSS_PATH="App.css"
    head= figlet_format("Payroll",font='3-d')
    BINDINGS = [('e', 'export','data Export'),('a', 'addemp','Add Employee Menu'),('t', 'view_tables','View Tables'),('u','update','Open Update Form'),('m','attend','Mark Attendance'),
                ('p','paymenu','Open Payroll Menu')]
    def compose(self):
        DB = dbtransit.Connection("database.db")
        fetcher = fetcher(DB.get_cursor())
        self.fetcher = fetcher
        
        yield Header()
        yield Label(self.head)
        yield Label("Press E to export data")
        yield Label("Press A to Add Employee Menu")
        yield Label("Press T to view tables")
        yield Label("Press U to open Update form ")
        yield Label("Press P to open Payroll menu ")
        yield Label("Press M to Mark Attendance")
        yield Footer()
        
    def action_export(self):
        self.app.push_screen(Exportdatascreen())
    def action_addemp(self):
        self.app.push_screen(Form())
    def action_view_tables(self):
        self.app.push_screen(Tableview())
    def action_update(self):
        self.app.push_screen(Update_form())
    def action_paymenu(self):
        self.app.push_screen(Payrollscreen())
    def action_attend(self):
        self.app.push_screen(Attendscreen())

class PayrollApp(App):
    '''The Main APP UI'''
    CSS_PATH = "App.css"
    BINDINGS = [('q','quit_app','Exit App')]
    def compose(self):
        yield Header(show_clock=True)
        # yield Static("Some Text")
        yield Menu(classes="Menu")
        # yield Thetable()
        yield Footer()
    def action_quit_app(self):
        self.exit()
            
        
if __name__ == '__main__':
    
    import dbtransit
    from data_management import fetcher
    # DB = dbtransit.Connection("database.db")
    # DB.createdatasturcture()
    # fetcher = fetcher(DB.get_cursor())
    # Entries = self.fetcher.viewdata("Attendance","In_Time","Out_Time")
    Testrun().run()
    # PayrollApp().run()