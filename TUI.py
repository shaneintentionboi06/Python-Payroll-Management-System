from textual.app import App,ComposeResult
from textual.widgets import Header,Footer,DataTable,Static,ListView,ListItem,Button,Select,Tabs,Tab,Label,Input
from textual.containers import ScrollableContainer,Container
from itertools import cycle
from textual import on 
from textual.screen import Screen,ModalScreen
from textual.notifications import Notification,Notify
# from textual.reactive import reactive

#THis is the Most of the reason I am doing this project and why I hate it at the same time

cursors = cycle(['column','row','cell','none'])

class Menu(Static):
    
    def compose(self):
        yield Static("Welcome")
        yield ListView(
            ListItem(Button("View Tables",id='table')),
            ListItem(Button("Export Employee Data",id='expemployee')),
            ListItem(Button("Update Employee Data",id='update')),
            ListItem(Button("Mark Attendance",id='attend')),
            ListItem(Button("Remove Employee",id='remove'))
        )

    @on(Button.Pressed,'#table')
    def calltable(self):
        self.app.push_screen(Tableview())
        
    @on(Button.Pressed,'#expemployee')
    def callexport(self):
        self.app.push_screen(Exportdatascreen())
    


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
    BINDINGS=[('escape','btn_back','Back to Main Menu')]
    def compose(self):
        Tables = list(Feteher._column_map_.keys())
        yield Header(show_clock=True)
        yield Tabs(*Tables)
        yield DataTable(id='Table')
        yield Footer()

    def action_btn_back(self):
        self.app.pop_screen()
    def _on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns(*Entries[0])
        table.add_rows(Entries[1:])
        table.cursor_type = next(cursors)
        table.zebra_stripes = True

    def key_c(self):
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)

class Exportinput(Static):
    def compose(self):
        yield Label("Export Data", id='title')
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
                Feteher.cursor.execute(f"select Name from Employee where Employee_ID = {ID}")
                return Feteher.cursor.fetchone()
        except Exception as err:
                return None
    
    @on(Input.Submitted,'#ID')
    def handle_input(self, event: Input.Submitted):
        Data = event.value
        try:
            Feteher.exporttempdata(Data)
            self.app.notify(f"Data Exported for Emp {Data}")
        except Exception as err:
            self.app.notify(f"Failed Error: {err}")
        self.app.pop_screen()
    @on(Input.Changed,'#ID')
    def on_input_changed(self, event: Input.Changed):
        Data = event.value
        Nameinput = self.query_one('#Namelabel')
        
        if Data.strip():
            Name = self.get_employee_ID(Data)[0]
            
            if Name:
                Nameinput.update(f"Found: {Name}")
            else:
                Nameinput.update(f"Not Found")
class Testrun(App):
    CSS_PATH="App.css"
    BINDINGS = [('e', 'export','Data Export')]
    def compose(self):
        yield Header()
        yield Label("Press e")
        yield Footer()
        
    def action_export(self):
        self.app.push_screen(Exportdatascreen())
    
class form(Screen):
    def compose(self):
        yield Header()
        yield Footer()
        
        yield Label('Name', id='namelabel')
        yield Input(placeholder='Name')
        
        yield Label('Department Name', id='deptnamelabel')
        yield Input(placeholder='Name')
        
        yield Label("Date of Joining",id='date_of_joininglabel')
        yield Input("Date of Joining",id='date_of_joining',value='today')
        
        yield Label("Designation",id='designationlabel')
        yield Input(id='Designation')

        yield Label("Contact",id='Contactlabel')
        yield Input(id='Contact')
        

class PayrollApp(App):
    '''The Main APP UI'''
    CSS_PATH = "App.css"
    BINDINGS = []
    def compose(self):
        yield Header(show_clock=True)
        # yield Static("Some Text")
        yield Menu(classes="Menu")
        # yield Thetable()
        yield Footer()
        
    def on_button_pressed(self,event: Button.Pressed):
        if event.button.id == 'table':
            
            # self.push_screen(Tableview())
            self.notify("Page Started")
            

    # def key_s(self):
        
    #     table = self.query_one(DataTable)

    def dataupdate(self):
        return Feteher.viewdata("Name","ContactNo")
        
if __name__ == '__main__':
    
    import dbtransit
    from datamanagement import fetcher
    DB = dbtransit.Connection("database.db")
    # DB.createdatasturcture()
    Feteher = fetcher(DB.get_cursor())
    Entries = Feteher.viewdata("Attendance","In_Time","Out_Time")
    PayrollApp().run()
    # Testrun().run()