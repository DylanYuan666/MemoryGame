import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QToolBar, QAction, QActionGroup, QMenu, 
                             QMessageBox, QGridLayout, QFrame)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QTimer
import Function  # 导入功能模块

class MaximizeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cards = []  # 存储卡片按钮
        self.init_ui()

    def init_ui(self):
        # 窗口基础设置（保持不变）
        self.setWindowTitle("数字匹配游戏")
        self.setMinimumSize(800, 600)
        self.showMaximized()
        
        # 创建工具栏（保持不变）
        self.create_toolbar()
        
        # 中心部件与布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(30)
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        
        # 添加初始界面组件
        self.add_initial_widgets()

    def create_game_board(self):
        """创建游戏卡片布局"""
        # 清空现有布局
        self.clear_layout(self.main_layout)
        
        # 根据难度获取行列数
        difficulty = self.get_current_difficulty()
        if difficulty == "4*4":
            rows, cols = 4, 4
        elif difficulty == "4*6":
            rows, cols = 4, 6
        else:  # 默认简单难度
            rows, cols = 3, 4
        
        # 使用Function生成随机数字数组
        self.number_array = Function.generate_random_array(rows, cols)
        
        # 创建网格布局放置卡片
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        self.main_layout.addLayout(grid_layout)
        
        # 存储卡片按钮的列表
        self.cards = []
        
        # 卡片样式（统一颜色）
        card_style = """
            QPushButton {
                background-color: #3498db;
                border-radius: 8px;
                font-size: 24px;
                font-weight: bold;
                color: transparent;  # 初始隐藏数字
                min-width: 80px;
                min-height: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f6dad;
            }
        """
        
        # 创建卡片按钮
        for i in range(rows):
            row_buttons = []
            for j in range(cols):
                btn = QPushButton()
                btn.setStyleSheet(card_style)
                btn.setProperty("row", i)  # 存储位置信息
                btn.setProperty("col", j)
                btn.setProperty("value", self.number_array[i][j])  # 存储数字值
                btn.clicked.connect(self.on_card_clicked)
                grid_layout.addWidget(btn, i, j)
                row_buttons.append(btn)
            self.cards.append(row_buttons)

    def add_initial_widgets(self):
        """添加初始界面组件"""
        # 清空现有布局
        self.clear_layout(self.main_layout)
        
        # 游戏标题
        title_label = QLabel("数字匹配游戏")
        title_label.setStyleSheet("""
            font-size: 40px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        # 游戏说明
        info_label = QLabel("找到相同数字并消除，挑战你的观察力！")
        info_label.setStyleSheet("""
            font-size: 18px; 
            color: #7f8c8d;
            margin-bottom: 40px;
        """)
        info_label.setAlignment(Qt.AlignCenter)
        
        # 开始游戏按钮
        start_btn = QPushButton("开始游戏")
        start_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px 40px;
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
        """)
        start_btn.clicked.connect(self.start_game)
        start_btn.setMinimumWidth(200)
        
        # 添加到布局
        self.main_layout.addWidget(title_label)
        self.main_layout.addWidget(info_label)
        self.main_layout.addWidget(start_btn, alignment=Qt.AlignCenter)


    def clear_layout(self, layout):
        """清空布局中的所有组件"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def on_card_clicked(self):
        """卡片点击事件处理（简单实现）"""
        btn = self.sender()
        # 显示卡片数字
        btn.setStyleSheet(btn.styleSheet().replace("color: transparent", f"color: white"))
        btn.setText(str(btn.property("value")))


    def create_toolbar(self):
        """创建工具栏，包含游戏常用功能"""
        # 创建工具栏
        toolbar = QToolBar("游戏工具栏", self)
        toolbar.setIconSize(QSize(24, 24))  # 设置图标大小
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 图标下显示文字
        toolbar.setMovable(False)  # 禁止工具栏拖动
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                padding: 5px;
            }
            QToolButton {
                font-size: 14px;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QToolButton:hover {
                background-color: #e9ecef;
            }
            QToolButton:pressed {
                background-color: #dee2e6;
            }
        """)
        
        # 添加工具栏到主窗口
        self.addToolBar(toolbar)
        
        # 1. 开始游戏动作
        start_action = QAction(
            QIcon.fromTheme("media-play"),  # 系统默认播放图标（跨平台兼容）
            "开始游戏", 
            self
        )
        start_action.setShortcut("Ctrl+S")  # 设置快捷键
        start_action.setStatusTip("开始新游戏")
        start_action.triggered.connect(self.start_game)
        toolbar.addAction(start_action)
        
        # 2. 重置游戏动作
        reset_action = QAction(
            QIcon.fromTheme("view-refresh"),  # 系统默认刷新图标
            "重置游戏", 
            self
        )
        reset_action.setShortcut("Ctrl+R")
        reset_action.setStatusTip("重置当前游戏")
        reset_action.triggered.connect(self.reset_game)
        toolbar.addAction(reset_action)
        
        # 添加分隔线
        toolbar.addSeparator()
        
        # 3. 难度选择（下拉菜单）
        difficulty_menu = QMenu("难度选择", self)
        self.difficulty_action = QAction("4*4", self, checkable=True, checked=True)
        easy_action = QAction("4*4", self, checkable=True)
        hard_action = QAction("4*6", self, checkable=True)
        
        # 难度互斥组
        difficulty_group = QActionGroup(self)
        difficulty_group.addAction(self.difficulty_action)
        difficulty_group.addAction(easy_action)
        difficulty_group.addAction(hard_action)
        
        difficulty_menu.addAction(self.difficulty_action)
        difficulty_menu.addAction(easy_action)
        difficulty_menu.addAction(hard_action)
        
        difficulty_action = QAction(
            QIcon.fromTheme("preferences-system"),  # 系统默认设置图标
            "难度选择", 
            self
        )
        difficulty_action.setMenu(difficulty_menu)
        toolbar.addAction(difficulty_action)
        
        # 添加分隔线
        toolbar.addSeparator()
        
        # 4. 帮助动作
        help_action = QAction(
            QIcon.fromTheme("help-browser"),  # 系统默认帮助图标
            "帮助", 
            self
        )
        help_action.setShortcut("F1")
        help_action.setStatusTip("查看游戏规则")
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)
        
        # 5. 退出动作
        exit_action = QAction(
            QIcon.fromTheme("application-exit"),  # 系统默认退出图标
            "退出", 
            self
        )
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("退出游戏")
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)
        
        # 设置状态栏（显示提示信息）
        self.statusBar().showMessage("欢迎来到数字匹配游戏！")

    def start_game(self):
        """开始游戏事件处理"""
        self.statusBar().showMessage(f"游戏开始 - 当前难度：{self.get_current_difficulty()}")
        self.create_game_board()  # 创建游戏卡片布局

    def reset_game(self):
        """重置游戏事件处理"""
        self.statusBar().showMessage(f"游戏已重置 - 当前难度：{self.get_current_difficulty()}")
        self.create_game_board()  # 重新创建游戏卡片
        QMessageBox.information(self, "重置成功", "游戏已重置，可重新开始！")


    def show_help(self):
        """显示帮助信息"""
        help_text = """
        数字匹配游戏规则：
        1. 游戏界面会显示若干带有数字的卡片
        2. 点击两张相同数字的卡片即可消除
        3. 消除所有卡片即可获胜
        4. 难度说明：
           - 简单：12张卡片，数字范围1-6
           - 中等：20张卡片，数字范围1-10
           - 困难：30张卡片，数字范围1-15
        5. 快捷键：
           - Ctrl+S：开始游戏
           - Ctrl+R：重置游戏
           - F1：查看帮助
           - Ctrl+Q：退出游戏
        """
        QMessageBox.information(self, "游戏帮助", help_text)

    def get_current_difficulty(self):
        """获取当前选择的难度"""
        for action in self.difficulty_action.actionGroup().actions():
            if action.isChecked():
                return action.text()
        return "简单"

if __name__ == "__main__":
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 设置应用字体（可选，让界面更美观）
    app.setFont(QFont("Microsoft YaHei", 10))
    
    # 创建主窗口并显示
    window = MaximizeMainWindow()
    window.show()  
    
    # 运行应用循环
    sys.exit(app.exec_())