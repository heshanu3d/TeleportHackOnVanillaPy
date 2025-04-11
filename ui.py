import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                            QVBoxLayout, QTableWidget, QTableWidgetItem, 
                            QPushButton, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

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
        self.table.setHorizontalHeaderLabels(["position", "x", "y", "z"])
        self.table.verticalHeader().setVisible(False)

        # 让表头可伸缩
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        total_width = 400
        col1_width = total_width * 3 // 5  # 第一列占一半
        other_col_width = total_width * 2 // 15  # 其他三列各占1/6
        self.table.setColumnWidth(0, col1_width)    # 第一列
        self.table.setColumnWidth(1, other_col_width)  # 第二列
        self.table.setColumnWidth(2, other_col_width)  # 第三列
        self.table.setColumnWidth(3, other_col_width)  # 第四列

        # 连接点击信号到槽函数
        self.table.cellClicked.connect(self.on_cell_clicked)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        # 禁用默认编辑功能
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # 填充表格数据
        self.load_data()
        
        # 创建重新加载按钮
        self.reload_btn = QPushButton("reload")
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
    def __init__(self, config, event):
        super().__init__()
        self.config = config
        self.event = event
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('TabView 电子表格示例')
        self.setGeometry(100, 100, 400, 800)
        self.setWindowIcon(QIcon(self.config.icon))
        
        self.tabs = QTabWidget()
        
        self.tab1 = SpreadsheetTab()
        self.tabs.addTab(self.tab1, "电子表格")
        
        self.tab2 = SecondTab()
        self.tabs.addTab(self.tab2, "其他功能")
        
        self.setCentralWidget(self.tabs)

def ui_main(config, event=None):
    app = QApplication(sys.argv)
    mainWin = MainWindow(config, event)
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    ui_main()