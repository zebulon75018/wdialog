# =============================
# requirements.txt (PyQt5)
# =============================
# =============================
# main.py — Version PyQt5 (QWebEngineView, plein écran, sans bord)
# =============================
import sys
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView
#from PyQt5.QtWebEngineCore import QWebEngineSettings


class KioskWindow(QWidget):
    def __init__(self, url: QUrl, parent=None):
        super().__init__(parent)

        # Fenêtre sans bord (ajoutez Qt.WindowStaysOnTopHint si vous voulez rester au-dessus)
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        #self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        # Layout plein écran
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.view = QWebEngineView(self)
        layout.addWidget(self.view)

        # Réglages WebEngine (JS, plugins, accès local)
        #s = self.view.settings()
        #s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        #s.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        #s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        #s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)

        # Charger l'URL
        self.view.load(url)

        # Raccourcis utiles
        QShortcut(QKeySequence(QKeySequence.StandardKey.Refresh), self, activated=self.reload)
        QShortcut(QKeySequence("Ctrl+R"), self, activated=self.reload)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, activated=self.close)

        # Passer en plein écran après affichage
        #QTimer.singleShot(0, self.showFullScreen)

    def reload(self):
        self.view.reload()


def main():
    app = QApplication(sys.argv)

    url = QUrl("http://localhost:5900")
    win = KioskWindow(url)
    win.show()  # basculera tout de suite en plein écran

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

