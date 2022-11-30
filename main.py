import time
from about import *
from pathlib import Path
from threading import Thread
from urllib.parse import quote
from os import walk, startfile
from webbrowser import open as web_open
from PySide6.QtGui import Qt, QIcon, QStatusTipEvent, QCursor, QAction, QGuiApplication
from PySide6.QtCore import Slot, QFileInfo
from ui_FileSearchEngine import Ui_MainWindow
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox,
    QTreeWidgetItem, QMenu, QFileIconProvider)
from viewerWindow import ViewerWindow
from playerWindow import PlayerWindow
from imageViewer import ImageViewer


class MainWindow(QMainWindow):

    file_num = 0       # 文件数目
    cache_list = []    # 缓存列表
    adding = False     # 添加中标志
    searching = False  # 搜索中标志

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_MainWindow()

        # 初始化界面
        self.ui.setupUi(self)

        self.viewer_window = ViewerWindow()  # 创建一个文本查看器窗口对象
        self.player_window = PlayerWindow()  # 创建一个播放器窗口对象
        self.image_window = ImageViewer()    # 创建一个图像查看器窗口对象

        # 设置TreeWidget每个标题的对应大小
        self.ui.outputTreeWidget.setColumnWidth(0, 200)
        self.ui.outputTreeWidget.setColumnWidth(1, 50)
        self.ui.outputTreeWidget.setColumnWidth(2, 80)
        self.ui.outputTreeWidget.setColumnWidth(3, 150)

        # 打开右键菜单策略
        self.ui.outputTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.outputTreeWidget.customContextMenuRequested.connect(self.right_clicked_func)  # 绑定事件

        # 双击响应策略
        self.ui.outputTreeWidget.doubleClicked.connect(self.double_clicked_func)  # 绑定事件

        # 绑定按钮功能
        self.ui.browseButton.clicked.connect(self.browse_dir)
        self.ui.searchButton.clicked.connect(self.start_search)

        # 动作事件绑定
        self.ui.actionHelp.triggered.connect(self.help)
        self.ui.actionAbout.triggered.connect(self.about)

        self.ui.actionTextViewer.triggered.connect(self.open_in_text_windows)
        self.ui.actionImageViewer.triggered.connect(self.open_in_image_windows)
        self.ui.actionPlayerViewer.triggered.connect(self.open_in_player_windows)

        self.ui.actionSearchWeb.triggered.connect(self.act_search_web)
        self.ui.actionSearchKey.triggered.connect(self.act_search_key)
        self.ui.actionSearchName.triggered.connect(self.act_search_name)
        self.ui.actionSearchType.triggered.connect(self.act_search_type)

    def act_search_key(self):
        """按照文件关键字寻找并做对应处理"""
        if self.searching:
            return
        self.change_widgets_status()
        self.ui.downLabel.setText("关键字")
        self.change_icon(self.ui.actionSearchKey)
        self.ui.downLineEdit.setPlaceholderText("请输入文件中特有的关键字")

    def act_search_name(self):
        """按照文件名称寻找并做对应处理"""
        if self.searching:
            return
        self.change_widgets_status()
        self.ui.downLabel.setText("名称：")
        self.change_icon(self.ui.actionSearchName)
        self.ui.downLineEdit.setPlaceholderText("请输入大概的文件名称")

    def act_search_type(self):
        """按照文件类型寻找并做对应处理"""
        if self.searching:
            return
        self.change_widgets_status()
        self.ui.downLabel.setText("类型：")
        self.change_icon(self.ui.actionSearchType)
        self.ui.downLineEdit.setPlaceholderText("请输入文件类型，列如exe")

    def act_search_web(self):
        """浏览器寻找并做对应处理"""
        if self.searching:
            return
        self.ui.downLabel.setText("")
        self.change_widgets_status(True)
        self.change_icon(self.ui.actionSearchWeb)
        self.ui.downLineEdit.setPlaceholderText("请输入要搜索的内容")

    def browse_dir(self):
        """选择目录，并输出到文本框中"""
        file_directory = QFileDialog.getExistingDirectory(self, "选择文件夹")
        # 判断如果file_directory有内容，则设置文本
        if file_directory:
            self.ui.upLineEdit.setText(file_directory)

    def start_search(self):
        """开始搜索按钮被点击，用多线程搜索文件"""
        # 如果为开始搜索并且不为添加中则取消搜索
        if self.ui.searchButton.text() == "取消搜索" and not self.adding:
            Thread(target=self.cancel_search).start()
            return
        # 判断是否在搜索中，如果不是，就行搜索，否则不执行
        if self.searching:
            msg = "搜索"
            if self.adding:
                msg = "添加"
            QMessageBox.information(self, "提示", "已经在努力地%s了......" % msg)
            return

        text = self.ui.upLineEdit.text()  # 获取输入框路径
        word = self.ui.downLabel.text().split("：")[0]  # 获取标签文本
        text_type = self.ui.downLineEdit.text()   # 获取输入框内容类型
        path = Path("C:/" if not text else text)  # 判断路径输入框内容，如果为空则用C:/，否则用文本里的路径

        # 判断路径是否有存在，如果路径不存在则提示并退出
        if not path.exists():
            QMessageBox.critical(self, "路径错误", "请检查路径后重试！")
            return

        # 判断type输入框是否有内容
        if not text_type:
            QMessageBox.warning(self, "警告", "请输入%s！" % word)
            return

        # 如果标签文本为空，则说明用了web搜索
        if not word:
            url = "https://www.baidu.com/s?wd=" + quote(text_type)
            Thread(target=lambda: web_open(url)).start()
            QMessageBox.information(self, "提示", "已启动浏览器")
            return

        self.searching = True  # 标志设为搜索中
        if self.file_num != 0:
            self.ui.outputTreeWidget.clear()  # 清理添加到treeWidget里的所有内容
        self.file_num = 0  # 文件数目清零
        self.ui.statusbar.showMessage("努力搜索中......")  # 显示开始搜索提示信息

        # 开始搜索转为取消搜索
        self.ui.searchButton.setText("取消搜索")

        # 根据类型创建线程搜索文件
        search_method = self.search_type
        if word == "名称":
            search_method = self.search_name
        elif word == "关键字":
            search_method = self.search_key

        # 开启线程搜索
        Thread(
            target=search_method,
            args=(path, text_type),
            daemon=True
        ).start()

    def search_type(self, file_path, file_type):
        """按照类型寻找文件"""
        file_type = '.' + file_type
        for path, _, files in walk(file_path):  # 遍历所有文件查找
            for file in files:
                if self.adding:
                    return
                if file.endswith(file_type) and not self.adding:
                    self.add_file(Path(path) / file)
        if not self.adding:
            self.finish()

    def search_key(self, file_path, key):
        """按照关键字寻找文件"""
        for path, _, files in walk(file_path):  # 遍历所有文件查找
            for file in files:
                if self.adding:
                    return
                try:
                    if key in open(path + '/' + file, mode='r', encoding="utf-8").read() and not self.adding:
                        self.add_file(Path(path) / file)
                except UnicodeDecodeError:
                    continue
        if not self.adding:
            self.finish()

    def search_name(self, file_path, name):
        """按照文件名寻找文件"""
        for path, _, files in walk(file_path):  # 遍历所有文件查找
            for file in files:
                if self.adding:
                    return
                if name in file and not self.adding:
                    self.add_file(Path(path) / file)
        if not self.adding:
            self.finish()

    def add_file(self, file):
        """保存文件路径到缓存列表
        :param file: Path类型的文件路径
        """
        self.cache_list.append(file)  # 添加到缓存列表
        self.file_num += 1
        self.ui.statusbar.showMessage("%s个对象，搜索中......" % format(self.file_num, ","))  # 更新文件数目显示

    def finish(self):
        """完成搜索后的处理"""
        self.adding = True
        self.ui.searchButton.setText("开始搜索")
        self.decompression()  # 解压缓存列表
        self.ui.statusbar.showMessage("处理完成，共%s个对象" % format(self.file_num, ","))  # 更新文件数目显示
        self.cache_list.clear()  # 清空缓存所有文件标记
        self.adding = False
        self.searching = False  # 所有线程结束恢复为为搜索状态

    def insert_row(self, content):
        """把获取的文件内容添加到TreeWidget
        :param content:格式：[文件名, 文件类型, 文件大小, 修改时间, 文件路径]
        """
        icon = QIcon(QFileIconProvider().icon(QFileInfo(content[-1])))  # 获取文件在系统下显示的图标
        item = QTreeWidgetItem(self.ui.outputTreeWidget, content)
        item.setIcon(0, icon)  # 设置图标
        item.setTextAlignment(2, Qt.AlignTrailing | Qt.AlignVCenter)  # 文件大小（索引为2）设置为水平右对齐
        item.setTextAlignment(3, Qt.AlignCenter | Qt.AlignVCenter)  # 修改时间（索引为3）设置为水平居中对齐
        self.ui.outputTreeWidget.insertTopLevelItems(0, [item])  # 添加内容

    def decompression(self):
        """把缓存列表里的内容解压到TreeWidget"""
        self.adding = True
        self.ui.statusbar.showMessage("搜索完成，添加中......")
        for file in self.cache_list:
            try:
                self.insert_row(self.get_file_inform(file))
            except FileNotFoundError:
                continue
        self.adding = False

    def process_trigger(self, q):
        """根据点击处理对应事件"""
        command = q.text()
        item = self.ui.outputTreeWidget.currentItem()
        path = item.text(4)
        if command == "打开":
            path = Path(path)
            self.open_file(path)
        elif command == "复制路径":
            # 设置剪贴板内容
            QGuiApplication.clipboard().setText(path)
            QMessageBox.information(self, "提示", "复制成功！")
        elif command == "打开文件路径":
            path = Path("/".join(path.split("\\")[:-1]))
            self.open_file(path)
        elif command == "打开于\"文本查看器\"":
            self.open_in_text_windows(path)
        elif command == "打开于\"音频播放器\"":
            self.open_in_player_windows(path, item.text(1))
        elif command == "打开于\"图像查看器\"":
            self.open_in_image_windows(path)

    def right_clicked_func(self):
        """定义treeWidget中item右键界面"""
        if self.file_num == 0:
            return
        pop_menu = QMenu()
        pop_menu.addAction(QAction(u"打开", self))
        pop_menu.addAction(QAction(u"打开文件路径", self))
        pop_menu.addAction(QAction(u"打开于\"文本查看器\"", self))
        pop_menu.addAction(QAction(u"打开于\"图像查看器\"", self))
        pop_menu.addAction(QAction(u"打开于\"音频播放器\"", self))
        pop_menu.addAction(QAction(u"复制路径", self))
        pop_menu.triggered.connect(self.process_trigger)  # 右键点击清空之后执行的操作
        pop_menu.exec(QCursor.pos())  # 执行之后菜单可以显示

    def double_clicked_func(self):
        """双击打开文件事件"""
        if self.file_num == 0:
            return
        item = self.ui.outputTreeWidget.currentItem()
        self.open_file(Path(item.text(4)))

    def open_file(self, path):
        """根据文件路径打开文件"""
        if path.exists():
            Thread(target=lambda: startfile(str(path))).start()
        else:
            QMessageBox.critical(self, "错误", "文件被移除")

    def open_in_text_windows(self, path=None):
        """打开文件查看器窗口"""
        self.viewer_window.show()
        if path:
            self.viewer_window.open_file(path)

    def open_in_player_windows(self, file_path=None, file_type=None):
        """打开播放器窗口"""
        if file_path:
            if file_type not in [
                ".mp4", ".mp3", ".wma", ".wmv", ".webm", ".avi",
                ".avf", ".mov", ".flac", ".m4v", ".mkv", ".f4v"
            ]:
                QMessageBox.warning(self, "警告", "不支持此类型文件\n请到'工具'->'音频播放器' 里查看具体支持类型")
                return
            self.player_window = PlayerWindow()  # 名称点击新建对象，防止堆积音乐
            self.player_window.open(file_path)
        self.player_window.show()  # 显示窗口

    def open_in_image_windows(self, path=None):
        """打开图片查看器窗口"""
        self.image_window.show()
        if path:
            self.image_window.load_file(path)

    def cancel_search(self):
        """取消搜索"""
        self.ui.searchButton.setText("开始搜索")
        self.finish()

    @Slot()
    def change_widgets_status(self, is_hide=False):
        """更改部件状态及窗口大小"""
        if is_hide:
            self.ui.upLabel.hide()
            self.ui.upLineEdit.hide()
            self.ui.browseButton.hide()
            self.ui.outputTreeWidget.hide()
            self.resize(self.geometry().width(), self.minimumHeight())
        else:
            self.ui.upLabel.show()
            self.ui.upLineEdit.show()
            self.ui.browseButton.show()
            self.ui.outputTreeWidget.show()

    @Slot()
    def change_icon(self, action):
        """改变图标"""
        off = QIcon("./icons/radio-circle.png")
        on = QIcon("./icons/radio-circle-marked.png")
        self.ui.actionSearchWeb.setIcon(off)
        self.ui.actionSearchKey.setIcon(off)
        self.ui.actionSearchName.setIcon(off)
        self.ui.actionSearchType.setIcon(off)
        action.setIcon(on)

    @Slot()
    def help(self):
        """显示帮助信息"""
        Thread(target=lambda: web_open(HElP)).start()

    @Slot()
    def about(self):
        """显示关于信息"""
        QMessageBox.about(self, "关于作者", ABOUT)

    @staticmethod
    def get_file_inform(file_path):
        """接受一个path类型的文件路径，获取文件详细信息"""
        # 处理文件大小并添加单位
        size = file_path.stat().st_size
        kb = size // 1000
        mb = round(kb / 1000, 1)
        if kb > 1000:
            size = f"{mb:,.1f} MB"
        else:
            size = f"{kb:,d} KB"

        file_type = file_path.suffix
        file_name = file_path.with_suffix("").name
        file_time = time.strftime("%Y/%m/%d  %H:%M", time.localtime(file_path.stat().st_mtime))

        return [file_name, file_type, size, file_time, str(file_path)]

    def event(self, QEvent):
        """覆盖父类函方法，为了克服将鼠标放置于菜单栏上状态栏就消失的问题"""
        if QEvent.type() == QEvent.StatusTip:
            if QEvent.tip() == "":
                if self.searching:
                    if self.adding:
                        message = "搜索完成，努力添加中，不是无响应哦......"
                    else:
                        message = "努力搜索中，不是无响应哦......"
                else:
                    message = "共%s个对象" % format(self.file_num, ",")
                QEvent = QStatusTipEvent(message)
        return super().event(QEvent)


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
