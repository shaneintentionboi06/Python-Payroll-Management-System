from textual.app import App,ComposeResult
from textual.widgets import Header,Footer,DataTable,Static
from textual.containers import ScrollableContainer
from itertools import cycle
#THis is the Most of the reason I am doing this project and why I hate it at the same time

cursors = cycle(['column','row','cell','none'])


class Dtable(Static):
    
    def compose(self):
        yield DataTable()

    def _on_mount(self):
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        table.add_columns(*ENTRIES[0])
        table.add_rows(ENTRIES[1:])
        
    # def key_c(self):
    #     table = self.query_one(DataTable)
    #     table.cursor_type = next(cursors)

class PayrollApp(App):
    '''The Main APP UI'''
    BINDINGS = [('c','key_c','Toggle Cursors')]
    def compose(self):
        yield Header(show_clock=True)
        yield Dtable()
        yield Footer()
    
    def key_c(self):
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)

        
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
    
    PayrollApp().run()