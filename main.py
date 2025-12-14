from TUI import PayrollApp
from data_management import Fetcher
from dbtransit import Connection

class Payroll(PayrollApp):
    def __init__(self,Database, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        self.database = Connection(Database=Database)
        self.fetcher = Fetcher(self.database._cursor_)
        super().__init__(driver_class, css_path, watch_css, ansi_color)

if __name__ == "__main__":
    App = Payroll(Database="database.db")
    App.run()