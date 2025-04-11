import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                            QVBoxLayout, QTableWidget, QTableWidgetItem, 
                            QPushButton, QHeaderView)
from PyQt5.QtCore import Qt

teleport_list='favlist.fav'

def get_favlist(file="favlist.fav"):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print('UnicodeDecodeError')
        pass

    out = []
    for line in lines:
        out.append(line.split('#'))

    return out

class SpreadsheetTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 主布局
        layout = QVBoxLayout()
        
        # 创建表格部件
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        # self.table.setRowCount(1000)
        
        # 设置表头
        self.table.setHorizontalHeaderLabels(["列1", "列2", "列3", "列4"])
        
        # 让表头可伸缩
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 连接点击信号到槽函数
        self.table.cellClicked.connect(self.on_cell_clicked)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        # 禁用默认编辑功能
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # 填充表格数据
        self.load_data()
        
        # 创建重新加载按钮
        self.reload_btn = QPushButton("重新加载数据")
        self.reload_btn.clicked.connect(self.reload_data)
        
        # 添加部件到布局
        layout.addWidget(self.table)
        layout.addWidget(self.reload_btn)
        
        # 设置布局
        self.setLayout(layout)
    
    def load_data(self):
        out = get_favlist()

        self.table.setRowCount(len(out))

        for row, data in enumerate(out):
            for col in range(4):
                item = QTableWidgetItem(data[col])
                
                # 设置文本居中
                item.setTextAlignment(Qt.AlignCenter)
                
                # 将项目添加到表格
                self.table.setItem(row, col, item)
    
    def reload_data(self):
        self.table.clearContents()

        self.load_data()

        print("数据已重新加载")

    def on_cell_clicked(self, row, column):
        print(f"点击了第 {row + 1} 行，第 {column + 1} 列")
        
        item = self.table.item(row, column)
        if item is not None:
            print(f"单元格内容: {item.text()}")

    def on_cell_double_clicked(self, row, column):
        print(f"双击了第 {row + 1} 行，第 {column + 1} 列")
        
        item = self.table.item(row, column)
        if item is not None:
            print(f"单元格内容: {item.text()}")

class SecondTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("这是第二个标签页"))
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('TabView 电子表格示例')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主Tab部件
        self.tabs = QTabWidget()
        
        # 添加第一个标签页（电子表格）
        self.tab1 = SpreadsheetTab()
        self.tabs.addTab(self.tab1, "电子表格")
        
        # 添加第二个标签页（示例）
        self.tab2 = SecondTab()
        self.tabs.addTab(self.tab2, "其他功能")
        
        # 设置中心部件
        self.setCentralWidget(self.tabs)

def ui_main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())