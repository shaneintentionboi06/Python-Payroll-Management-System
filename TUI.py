from textual.app import App,ComposeResult
from textual.widgets import Header,Footer,DataTable,Static,ListView,ListItem,Button
from textual.containers import ScrollableContainer,Container
from itertools import cycle
from textual import on
from textual.screen import Screen
# from textual.reactive import reactive

#THis is the Most of the reason I am doing this project and why I hate it at the same time

cursors = cycle(['column','row','cell','none'])

class Menu(Static):
    
    def compose(self):
        yield Static("Welcome")
        yield ListView(
            ListItem(Button("View Tables",id='table')),
            ListItem(Button("View Employee Data",id='employee')),
            ListItem(Button("Update Employee Data",id='update')),
            ListItem(Button("Mark Attendance",id='attend')),
            ListItem(Button("Remove Employee",id='remove'))
        )

    @on(Button.Pressed,'#table')
    def calltable(self):
        self.mount(Tableview())
            


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
        yield Header(show_clock=True)
        yield Container(
            DataTable(id='Tables_view')
        )
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



class PayrollApp(App):
    '''The Main APP UI'''
    CSS_PATH = "App.css"
    BINDINGS = [('c','key_c','Toggle Cursors')]
    def compose(self):
        yield Header(show_clock=True)
        # yield Static("Some Text")
        yield Menu(classes="Menu")
        # yield Thetable()
        yield Footer()
        
    def on_button_pressed(self,event: Button.Pressed):
        if event.button.id == 'table':
            self.push_screen(Tableview())
    

    # def key_s(self):
        
    #     table = self.query_one(DataTable)

    def dataupdate(self):
        return Feteher.viewdata("Name","ContactNo")
        
if __name__ == '__main__':
    ENTRIES = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),]
    import dbtransit
    from datamanagement import fetcher
    DB = dbtransit.Connection("database.db")
    DB.createdatasturcture()
    Feteher = fetcher(DB.get_cursor())
    Entries = Feteher.viewdata("Attendance","In_Time","Out_Time")
    PayrollApp().run()