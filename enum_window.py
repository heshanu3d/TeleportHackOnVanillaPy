import win32gui, win32con, win32api
import time, math, random
import psutil
import win32process

class Hwnds():
    def __init__(self, proc_name=""):
        self.windows = {}
        self.proc_name = proc_name
    def callback(self, hwnd, extra):
        self.windows = extra
        temp = []
        temp.append(hwnd)
        temp.append(win32gui.GetClassName(hwnd))
        temp.append(win32gui.GetWindowText(hwnd))
        self.windows[hwnd] = temp
    def get_hwnds(self):
        win32gui.EnumWindows(self.callback, self.windows)
        hwnds = []
        for item in self.windows:
            # if "main" in self.windows[item][2]:
            #     print(self.windows[item][2])
            if (self.windows[item][2] == self.proc_name):
                # print(self.windows[item])
                hwnds.append(item)
        return hwnds

class Pids():
    def __init__(self, proc_name=""):
        self.proc_name = proc_name
    def get_pids(self):
        pids = []
        for proc in psutil.process_iter():
            if self.proc_name in proc.name():
                pids.append(proc.pid)
        return pids
    def get_pid_by_hwnd(self, hwnd):
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid

class HwndPids():
    def __init__(self, proc_name=""):
        self.proc_name = proc_name
    def get_hwnd_pids(self):
        hwnds_pids = []
        hwnds = Hwnds(self.proc_name).get_hwnds()
        pids = Pids()
        for hwnd in hwnds:
            hwnds_pids.append([hwnd, pids.get_pid_by_hwnd(hwnd)])
        return hwnds_pids


if __name__ == '__main__':

    print("Enumerating all windows...")

    obj = Hwnds("魔兽世界")
    for hwnd in obj.get_hwnds():
        print("魔兽世界", hwnd)

    pids = Pids("ctm")
    for pid in pids.get_pids():
        print("ctm", pid)

    pids = Pids()
    for hwnd in obj.get_hwnds():
        print("ctm", pids.get_pid_by_hwnd(hwnd))

    hp = HwndPids("魔兽世界")
    for hwnds_pid in hp.get_hwnd_pids():
        print(hwnds_pid)