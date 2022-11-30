"""参考于Qt官网：https://doc.qt.io/qtforpython/examples/example_widgets__imageviewer.html"""
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel,
                               QMainWindow, QMessageBox, QScrollArea,
                               QSizePolicy)
from PySide6.QtGui import (QColorSpace,
                           QImageReader, QImageWriter, QKeySequence,
                           QPalette, QPainter, QPixmap, QGuiApplication)
from PySide6.QtCore import QDir, QStandardPaths, Qt, Slot


class ImageViewer(QMainWindow):

    is_full = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图像查看器")
        self._scale_factor = 1.0
        self._first_file_dialog = True
        self._image_label = QLabel()
        self._image_label.setBackgroundRole(QPalette.Base)
        self._image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._image_label.setScaledContents(True)

        self._scroll_area = QScrollArea()
        self._scroll_area.setBackgroundRole(QPalette.Dark)
        self._scroll_area.setWidget(self._image_label)
        self._scroll_area.setVisible(False)
        self.setCentralWidget(self._scroll_area)
        self._create_actions()
        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)

    def load_file(self, fileName):
        reader = QImageReader(fileName)
        reader.setAutoTransform(True)
        new_image = reader.read()
        native_filename = QDir.toNativeSeparators(fileName)
        if new_image.isNull():
            error = reader.errorString()
            QMessageBox.information(self, QGuiApplication.applicationDisplayName(),
                                    f"无法加载 {native_filename}： {error}")
            return False
        self._set_image(new_image)
        self.setWindowFilePath(fileName)

        w = self._image.width()
        h = self._image.height()
        d = self._image.depth()
        color_space = self._image.colorSpace()
        description = color_space.description() if color_space.isValid() else "未知"
        message = f'打开 "{native_filename}"，{w}x{h}，描述：{d} ({description})'
        self.statusBar().showMessage(message)
        return True

    def _set_image(self, new_image):
        self._image = new_image
        if self._image.colorSpace().isValid():
            self._image.convertToColorSpace(QColorSpace.SRgb)
        self._image_label.setPixmap(QPixmap.fromImage(self._image))
        self._scale_factor = 1.0

        self._scroll_area.setVisible(True)
        self._print_act.setEnabled(True)
        self._fit_to_window_act.setEnabled(True)
        self._full_to_screen.setEnabled(True)
        self._update_actions()

        if not self._fit_to_window_act.isChecked():
            self._image_label.adjustSize()

    def _save_file(self, fileName):
        writer = QImageWriter(fileName)

        native_filename = QDir.toNativeSeparators(fileName)
        if not writer.write(self._image):
            error = writer.errorString()
            message = f"无法保存 {native_filename}: {error}"
            QMessageBox.information(self, QGuiApplication.applicationDisplayName(),
                                    message)
            return False
        self.statusBar().showMessage(f'保存至 "{native_filename}"')
        return True

    @Slot()
    def _open(self):
        dialog = QFileDialog(self, "打开文件")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptOpen)
        while (dialog.exec() == QDialog.Accepted
               and not self.load_file(dialog.selectedFiles()[0])):
            pass

    @Slot()
    def _save_as(self):
        dialog = QFileDialog(self, "另存为")
        self._initialize_image_filedialog(dialog, QFileDialog.AcceptSave)
        while (dialog.exec() == QDialog.Accepted
               and not self._save_file(dialog.selectedFiles()[0])):
            pass

    @Slot()
    def _print_(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QDialog.Accepted:
            with QPainter(printer) as painter:
                pixmap = self._image_label.pixmap()
                rect = painter.viewport()
                size = pixmap.size()
                size.scale(rect.size(), Qt.KeepAspectRatio)
                painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                painter.setWindow(pixmap.rect())
                painter.drawPixmap(0, 0, pixmap)

    @Slot()
    def _copy(self):
        QGuiApplication.clipboard().setImage(self._image)

    @Slot()
    def _paste(self):
        new_image = QGuiApplication.clipboard().image()
        if new_image.isNull():
            self.statusBar().showMessage("剪切板里没有图片内容，可以按 'PrtScn' 类似的按键打印屏幕内容，获取图片")
        else:
            self._set_image(new_image)
            self.setWindowFilePath('')
            w = new_image.width()
            h = new_image.height()
            d = new_image.depth()
            message = f"从剪贴板获取图像，{w}x{h}，描述: {d}"
            self.statusBar().showMessage(message)

    @Slot()
    def _zoom_in(self):
        self._scale_image(1.25)

    @Slot()
    def _zoom_out(self):
        self._scale_image(0.8)

    @Slot()
    def _normal_size(self):
        self._image_label.adjustSize()
        self._scale_factor = 1.0

    @Slot()
    def _fit_to_window(self):
        fit_to_window = self._fit_to_window_act.isChecked()
        self._scroll_area.setWidgetResizable(fit_to_window)
        if not fit_to_window:
            self._normal_size()
        self._update_actions()

    @Slot()
    def _full_screen(self):
        self._scroll_area.setWidgetResizable(True)
        self.menuBar().hide()
        self.statusBar().hide()
        self.showFullScreen()
        self.is_full = True
        QMessageBox.information(self, "提示", "按ESC退出全屏")

    def _create_actions(self):
        file_menu = self.menuBar().addMenu("&文件")

        self._open_act = file_menu.addAction("&打开")
        self._open_act.triggered.connect(self._open)
        self._open_act.setShortcut(QKeySequence.Open)

        self._save_as_act = file_menu.addAction("&另存为")
        self._save_as_act.triggered.connect(self._save_as)
        self._save_as_act.setEnabled(False)

        self._print_act = file_menu.addAction("&打印")
        self._print_act.triggered.connect(self._print_)
        self._print_act.setShortcut(QKeySequence.Print)
        self._print_act.setEnabled(False)

        file_menu.addSeparator()

        self._exit_act = file_menu.addAction("退出")
        self._exit_act.triggered.connect(self.close)
        self._exit_act.setShortcut("Ctrl+Q")

        edit_menu = self.menuBar().addMenu("&编辑")

        self._copy_act = edit_menu.addAction("&复制")
        self._copy_act.triggered.connect(self._copy)
        self._copy_act.setShortcut(QKeySequence.Copy)
        self._copy_act.setEnabled(False)

        self._paste_act = edit_menu.addAction("&粘贴")
        self._paste_act.triggered.connect(self._paste)
        self._paste_act.setShortcut(QKeySequence.Paste)

        view_menu = self.menuBar().addMenu("&视图")

        self._zoom_in_act = view_menu.addAction("放大 (25%)")
        self._zoom_in_act.setShortcut(QKeySequence.ZoomIn)
        self._zoom_in_act.triggered.connect(self._zoom_in)
        self._zoom_in_act.setEnabled(False)

        self._zoom_out_act = view_menu.addAction("缩小 (25%)")
        self._zoom_out_act.triggered.connect(self._zoom_out)
        self._zoom_out_act.setShortcut(QKeySequence.ZoomOut)
        self._zoom_out_act.setEnabled(False)

        self._normal_size_act = view_menu.addAction("&恢复正常尺寸")
        self._normal_size_act.triggered.connect(self._normal_size)
        self._normal_size_act.setShortcut("Ctrl+S")
        self._normal_size_act.setEnabled(False)

        view_menu.addSeparator()

        self._full_to_screen = view_menu.addAction("&全屏显示")
        self._full_to_screen.triggered.connect(self._full_screen)
        self._full_to_screen.setShortcut(QKeySequence(Qt.Key_F11))
        self._full_to_screen.setEnabled(False)

        self._fit_to_window_act = view_menu.addAction("&缩放至窗口")
        self._fit_to_window_act.triggered.connect(self._fit_to_window)
        self._fit_to_window_act.setEnabled(False)
        self._fit_to_window_act.setCheckable(True)
        self._fit_to_window_act.setShortcut("Ctrl+F")

    def _update_actions(self):
        has_image = not self._image.isNull()
        self._save_as_act.setEnabled(has_image)
        self._copy_act.setEnabled(has_image)
        enable_zoom = not self._fit_to_window_act.isChecked()
        self._zoom_in_act.setEnabled(enable_zoom)
        self._zoom_out_act.setEnabled(enable_zoom)
        self._normal_size_act.setEnabled(enable_zoom)

    def _scale_image(self, factor):
        self._scale_factor *= factor
        new_size = self._scale_factor * self._image_label.pixmap().size()
        self._image_label.resize(new_size)

        self._adjust_scrollbar(self._scroll_area.horizontalScrollBar(), factor)
        self._adjust_scrollbar(self._scroll_area.verticalScrollBar(), factor)

        self._zoom_in_act.setEnabled(self._scale_factor < 3.0)
        self._zoom_out_act.setEnabled(self._scale_factor > 0.333)

    @staticmethod
    def _adjust_scrollbar(scrollBar, factor):
        pos = int(factor * scrollBar.value()
                  + ((factor - 1) * scrollBar.pageStep() / 2))
        scrollBar.setValue(pos)

    def _initialize_image_filedialog(self, dialog, acceptMode):
        if self._first_file_dialog:
            self._first_file_dialog = False
            locations = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
            directory = locations[-1] if locations else QDir.currentPath()
            dialog.setDirectory(directory)

        mime_types = [m.data().decode('utf-8') for m in QImageWriter.supportedMimeTypes()]
        mime_types.sort()

        dialog.setMimeTypeFilters(mime_types)
        dialog.selectMimeTypeFilter("image/jpeg")
        dialog.setAcceptMode(acceptMode)
        if acceptMode == QFileDialog.AcceptSave:
            dialog.setDefaultSuffix("jpg")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.is_full:
            self._fit_to_window()
            self._normal_size()
            self.menuBar().show()
            self.statusBar().show()
            self.showNormal()
            self.is_full = False


if __name__ == '__main__':
    app = QApplication([])
    image_viewer = ImageViewer()
    image_viewer.show()
    app.exec()
