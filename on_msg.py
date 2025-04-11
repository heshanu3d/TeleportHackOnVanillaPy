
def on_cell_single_click(self, row, column):
    pass
def on_cell_single_doubleclick(self, row, column):
    pass
def on_reload():
    pass
def on_teleport():
    pass
def on_insert():
    pass
def on_append():
    pass
def on_add():
    pass
def on_delete():
    pass
def on_save():
    pass

class Event:
    def __init__(self, mgr):
        self.mgr = mgr
        self.__dict__['cell_single_click'] = on_cell_single_click
        self.__dict__['cell_single_doubleclick'] = on_cell_single_doubleclick
        self.__dict__['reload'] = on_reload
        self.__dict__['teleport'] = on_teleport
        self.__dict__['insert'] = on_insert
        self.__dict__['append'] = on_append
        self.__dict__['add'] = on_add
        self.__dict__['delete'] = on_delete
        self.__dict__['save'] = on_save
