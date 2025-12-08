from textual.app import App,ComposeResult
from textual.widgets import Header,Footer,DataTable
from textual.containers import ScrollableContainer

#THis is the Most of the reason I am doing this project and why I hate it at the same time

class PayrollApp(App):
    '''The Main APP UI'''
    
    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        
if __name__ == '__main__':
    PayrollApp().run()