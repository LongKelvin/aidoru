from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.Application import Application
from src.utils import clearLayout, dropShadow

class AlbumLabel(QWidget):

    def __init__(self, parent, album):
        QWidget.__init__(self, parent)
        self.album = album
        self.initUI()

    def initUI(self):
        size = QSize(165, 200)
        self.setMinimumSize(size)
        self.setMaximumSize(size)
        self.resize(size)

        width = 150

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.coverLabelContainer = coverLabelContainer = QWidget(self)
        coverLabelContainer.setObjectName("cover-label")
        coverLabelContainer.setMinimumSize(QSize(width, width))
        coverLabelContainer.setMaximumSize(QSize(width, width))
        coverLabelContainer.setGraphicsEffect(dropShadow())
        coverLabelContainerL = QHBoxLayout(coverLabelContainer)
        coverLabelContainerL.setSpacing(0)
        coverLabelContainerL.setContentsMargins(0, 0, 0, 0)
        coverLabelContainer.setLayout(coverLabelContainerL)
        layout.addWidget(coverLabelContainer)

        if self.album.image:
            self.coverLabel = coverLabel = QLabel(self)
            pixmap = QPixmap(self.album.image)
            if pixmap.width() >= pixmap.height():
                pixmap = pixmap.scaledToWidth(width, Qt.SmoothTransformation)
            else:
                pixmap = pixmap.scaledToHeight(width, Qt.SmoothTransformation)
            coverLabel.setPixmap(pixmap)
            coverLabel.setAlignment(Qt.AlignCenter)
            coverLabelContainerL.addWidget(coverLabel)

        self.titleLabel = QLabel(self.album.title, self)
        self.titleLabel.setMaximumSize(QSize(self.width(), self.titleLabel.height()))
        layout.addWidget(self.titleLabel)

        self.artistLabel = QLabel(self.album.artist, self)
        self.artistLabel.setMaximumSize(QSize(self.width(), self.artistLabel.height()))
        self.artistLabel.setWordWrap(True)
        layout.addWidget(self.artistLabel)

    def mousePressEvent(self, event):
        Application.mainWindow.setSong(self.album.medias[0])

class SearchView(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName("search-view")
        self.initUI()
        self.bindEvents()

    def initUI(self):
        clayout = QVBoxLayout()
        clayout.setContentsMargins(5,5,5,0)
        clayout.setSpacing(0)
        self.setLayout(clayout)
        container = QWidget()
        clayout.addWidget(container)

        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0,0,0,0)
        vlayout.setSpacing(0)
        container.setLayout(vlayout)

        layoutw = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layoutw.setLayout(layout)
        vlayout.addWidget(layoutw)

        self.searchBox = searchBox = QLineEdit()
        layout.addWidget(searchBox)

        self.openButton = QPushButton("Open")
        layout.addWidget(self.openButton)

        self.navbarPadding = QWidget() # HACK
        #self.navbarPadding.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addWidget(self.navbarPadding)

        #
        self.albumScroll = scrollArea = QScrollArea()
        scrollArea.hide()
        scrollArea.setMinimumSize(QSize(0, 200))
        scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scrollArea.setWidgetResizable(True)
        scrollArea.installEventFilter(self)
        vlayout.addWidget(scrollArea)

        self.albumContainer = QWidget(scrollArea)
        scrollArea.setWidget(self.albumContainer)

        self.nchild = 0
        self.albumLabels = []

    # album add
    def addAlbumLabel(self, albumLabel):
        albumLabel.setParent(self.albumContainer)
        albumLabel.move(QPoint(self.nchild*albumLabel.width(), 0))
        self.albumLabels.append(albumLabel)
        self.nchild += 1
        self.albumContainer.setMinimumSize(self.nchild*albumLabel.width(), 0)
        albumLabel.show()

    # events
    def bindEvents(self):
        self.searchBox.textChanged.connect(self.textChanged)
        self.openButton.clicked.connect(self.openButtonClicked)

    def resizeEvent(self, event):
        mediaPlayer = Application.mainWindow.centralWidget()
        size = QSize(mediaPlayer.windowDecorations.width(), 0)
        self.navbarPadding.setMinimumSize(size)
        self.navbarPadding.resize(size)

    def textChanged(self, text):
        self.parentWidget().tableWidget.filterText = text
        self.parentWidget().tableWidget.sortAndFilter()

        self.nchild = 0
        for albumLabel in self.albumLabels:
            albumLabel.deleteLater()
        self.albumLabels.clear()

        albums = [v for k, v in Application.mainWindow.albums.items() if text in v.title.lower()]
        if not albums:
            self.albumScroll.hide()
            return
        self.albumScroll.show()
        albums.sort()

        if len(albums) <= 5:
            for album in albums:
                self.addAlbumLabel(AlbumLabel(self, album))
        else:
            albums = iter(albums)
            def iteration():
                if self.searchBox.text() != text:
                    return
                try:
                    self.addAlbumLabel(AlbumLabel(self, next(albums)))
                    QTimer.singleShot(1, iteration)
                except StopIteration:
                    return
            iteration()

    def openButtonClicked(self):
        print(self.searchBox.text())
        Application.mainWindow.setSong(self.searchBox.text())

    # album events
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            event.ignore()
        return False

    def wheelEvent(self, event):
        scrollBar = self.albumScroll.horizontalScrollBar()
        scrollBar.setValue(scrollBar.value()-event.angleDelta().y())

    # slots
    def toggleVisible(self):
        from .MediaPlayer import MediaPlayer
        if self.parentWidget().parentWidget().mode == MediaPlayer.FILE_LIST_MODE:
            self.setVisible(not self.isVisible())
        else:
            self.parentWidget().parentWidget().setMode(MediaPlayer.FILE_LIST_MODE)
            self.show()
        if self.isVisible():
            self.searchBox.setFocus(True)
