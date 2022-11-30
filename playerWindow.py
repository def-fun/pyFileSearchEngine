"""参考于Qt官网：https://doc.qt.io/qtforpython/examples/example_multimedia__player.html"""
import sys
from PySide6.QtCore import QStandardPaths, Qt, Slot, QUrl
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,
                               QMainWindow, QSlider, QStyle, QToolBar)
from PySide6.QtMultimedia import (QAudioOutput, QMediaFormat, QMediaPlayer)
from PySide6.QtMultimediaWidgets import QVideoWidget

AVI = "video/x-msvideo"  # AVI

MP4 = 'video/mp4'


def get_supported_mime_types():
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result


class PlayerWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        available_geometry = self.screen().availableGeometry()
        self.resize(available_geometry.width() / 3, available_geometry.height() / 2)

        self._playlist = []
        self._playlist_index = -1
        self.setToolTip("音频播放器")
        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)

        self._player.errorOccurred.connect(self._player_error)

        tool_bar = QToolBar()
        self.addToolBar(tool_bar)

        play_menu = self.menuBar().addMenu("&播放")
        file_menu = self.menuBar().addMenu("&程序")

        icon = QIcon("./icons/folder-open.png")
        open_action = QAction(icon, "&打开", self, triggered=self.open)
        tool_bar.addAction(open_action)
        icon = QIcon.fromTheme("application-exit")
        exit_action = QAction(icon, "退出", self, triggered=self.close)
        file_menu.addAction(exit_action)

        style = self.style()
        icon = QIcon.fromTheme("media-playback-start.png",
                               style.standardIcon(QStyle.SP_MediaPlay))
        self._play_action = tool_bar.addAction(icon, "播放")
        self._play_action.triggered.connect(self._player.play)
        play_menu.addAction(self._play_action)

        icon = QIcon.fromTheme("media-skip-backward-symbolic.svg",
                               style.standardIcon(QStyle.SP_MediaSkipBackward))
        self._previous_action = tool_bar.addAction(icon, "上一首")
        self._previous_action.triggered.connect(self.previous_clicked)
        play_menu.addAction(self._previous_action)

        icon = QIcon.fromTheme("media-playback-pause.png",
                               style.standardIcon(QStyle.SP_MediaPause))
        self._pause_action = tool_bar.addAction(icon, "暂停")
        self._pause_action.triggered.connect(self._player.pause)
        play_menu.addAction(self._pause_action)

        icon = QIcon.fromTheme("media-skip-forward-symbolic.svg",
                               style.standardIcon(QStyle.SP_MediaSkipForward))
        self._next_action = tool_bar.addAction(icon, "下一首")
        self._next_action.triggered.connect(self.next_clicked)
        play_menu.addAction(self._next_action)

        icon = QIcon.fromTheme("media-playback-stop.png",
                               style.standardIcon(QStyle.SP_MediaStop))
        self._stop_action = tool_bar.addAction(icon, "停止")
        self._stop_action.triggered.connect(self._ensure_stopped)
        play_menu.addAction(self._stop_action)

        self._volume_slider = QSlider()
        self._volume_slider.setOrientation(Qt.Horizontal)
        self._volume_slider.setMinimum(0)
        self._volume_slider.setMaximum(100)
        available_width = self.screen().availableGeometry().width()
        self._volume_slider.setFixedWidth(available_width / 10)
        self._volume_slider.setValue(self._audio_output.volume())
        self._volume_slider.setTickInterval(10)
        self._volume_slider.setTickPosition(QSlider.TicksBelow)
        self._volume_slider.setToolTip("音量")
        self._volume_slider.valueChanged.connect(self._audio_output.setVolume)
        tool_bar.addWidget(self._volume_slider)

        self._video_widget = QVideoWidget()
        self.setCentralWidget(self._video_widget)
        self._player.playbackStateChanged.connect(self.update_buttons)
        self._player.setVideoOutput(self._video_widget)

        self.update_buttons(self._player.playbackState())
        self._mime_types = []

    def closeEvent(self, event):
        self._ensure_stopped()
        event.accept()

    @Slot()
    def open(self, file_path=None):
        self._ensure_stopped()

        file_dialog = QFileDialog(self)

        is_windows = sys.platform == "win32"
        if not self._mime_types:
            self._mime_types = get_supported_mime_types()
            if is_windows and AVI not in self._mime_types:
                self._mime_types.append(AVI)
            elif MP4 not in self._mime_types:
                self._mime_types.append(MP4)

        file_dialog.setMimeTypeFilters(self._mime_types)

        default_mimetype = AVI if is_windows else MP4
        if default_mimetype in self._mime_types:
            file_dialog.selectMimeTypeFilter(default_mimetype)

        movies_location = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_location)

        if file_path:
            url = QUrl.fromLocalFile(file_path)
            self.play(url)
            return

        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self.play(url)

    @Slot()
    def play(self, url):
        self._playlist.append(url)
        self._playlist_index = len(self._playlist) - 1
        self._player.setSource(url)
        self._player.play()

    @Slot()
    def _ensure_stopped(self):
        if self._player.playbackState() != QMediaPlayer.StoppedState:
            self._player.stop()

    @Slot()
    def previous_clicked(self):
        if self._player.position() <= 5000 and self._playlist_index > 0:
            self._playlist_index -= 1
            self._playlist.previous()
            self._player.setSource(self._playlist[self._playlist_index])
        else:
            self._player.setPosition(0)

    @Slot()
    def next_clicked(self):
        if self._playlist_index < len(self._playlist) - 1:
            self._playlist_index += 1
            self._player.setSource(self._playlist[self._playlist_index])

    @Slot("QMediaPlayer::PlaybackState")
    def update_buttons(self, state):
        media_count = len(self._playlist)
        self._play_action.setEnabled(media_count > 0
                                     and state != QMediaPlayer.PlayingState)
        self._pause_action.setEnabled(state == QMediaPlayer.PlayingState)
        self._stop_action.setEnabled(state != QMediaPlayer.StoppedState)
        self._previous_action.setEnabled(self._player.position() > 0)
        self._next_action.setEnabled(media_count > 1)

    def show_status_message(self, message):
        self.statusBar().showMessage(message, 5000)

    @Slot("QMediaPlayer::Error", str)
    def _player_error(self, error):
        error_string = "该文件目前无法正常解析"
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)


if __name__ == '__main__':
    app = QApplication([])
    main_window = PlayerWindow()
    main_window.show()
    app.exec()
