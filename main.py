from TUI import PayrollApp
from data_management import fetcher
from dbtransit import Connection

class Payroll(PayrollApp,Connection,fetcher):
    def __init__(self,Database, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        Connection.__init__(self,Database=Database)
        self.Fetcher = fetcher(self._database_.cursor())
        super().__init__(driver_class, css_path, watch_css, ansi_color)

if __name__ == "__main__":
    App = Payroll(Database="database.db")
    App.run()