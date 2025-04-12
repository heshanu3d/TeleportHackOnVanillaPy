from log import *

def on_cell_single_clicked(mgr, self, row, column):
    pos = self.table.item(row, 0).text()
    x   = self.table.item(row, 1).text()
    y   = self.table.item(row, 2).text()
    z   = self.table.item(row, 3).text()
    print(pos, x, y, z)
def on_cell_double_clicked(mgr, self, row, column):
    pos = self.table.item(row, 0).text()
    x   = self.table.item(row, 1).text()
    y   = self.table.item(row, 2).text()
    z   = self.table.item(row, 3).text()
    # hack = mgr.get_hack('Mms')
    for name, info in mgr.get_hack_infos().items():
        if name == "Mms" or name == "快乐站士":
            hack = info[0]
            hack.set_pos(x, y, z)
            playername = hack.playername
            logger.info(f'{playername} teleported to {pos} : |{x}|{y}|{z}|')
def on_reload(mgr):
    pass
def on_teleport(mgr):
    pass
def on_insert(mgr):
    pass
def on_append(mgr):
    pass
def on_add(mgr):
    pass
def on_delete(mgr):
    pass
def on_save(mgr):
    pass

class Event:
    def __init__(self, mgr):
        self.mgr = mgr
        self.__dict__['cell_single_clicked'] = on_cell_single_clicked
        self.__dict__['cell_double_clicked'] = on_cell_double_clicked
        self.__dict__['reload'] = on_reload
        self.__dict__['teleport'] = on_teleport
        self.__dict__['insert'] = on_insert
        self.__dict__['append'] = on_append
        self.__dict__['add'] = on_add
        self.__dict__['delete'] = on_delete
        self.__dict__['save'] = on_save
    def trigger(self, func, *args):
        func(self.mgr, *args)

# mgr = []
# def trigger(func, *args):
#     func(mgr, *args)
# def cell_single_clicked(mgr, row, column):
#     print(row, column)
# trigger(cell_single_clicked, 1, 2)