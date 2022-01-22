"""
Business view
I have 10 words with the youtube links
I start the app
I hear the sequence of 10 x 10 sec audio for those 10 words
After that it stops playing. I enjoy the process and better know those 10 words
Then, I repeat this process with the other 10, 20, 50 words, with some repetition cycle and train myself
  to know it better and better
"""

"""
# Engineering view
1. A component of main class which draws a main window (eng_complex_interface.py or eng_autorefresh.py)
2. Class(es) for draw the web page with a video content (eng_plays_automatically.py)
3. Class Timer for destroying / recreating page with the next word (eng_autorefresh.py)
4. The list of words with links to the proper youtube video (I need to prepare it)
"""


import os
import sys
from PyQt5.Qt import QApplication, QMainWindow
from PyQt5.QtCore import QRect, QUrl, QCoreApplication, QMetaObject, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt5.QtWidgets import QApplication

words = [
    ["poverty", "https://www.youtube.com/embed/15-DE4i30m8?autoplay=1&mute=0&start=202&end=212;rel=0"],
    ["promenade", "https://www.youtube.com/embed/qM0uOAqrVb0?autoplay=1&mute=0&start=653&end=663;rel=0"],
    ["sameness", "https://www.youtube.com/embed/o1Z4F4e2Bw4?autoplay=1&mute=0&start=589&end=599;rel=0"],
    ["allay", "https://www.youtube.com/embed/a0KtqDTmDa4?autoplay=1&mute=0&start=2731&end=2741;rel=0"],
    ["ramble", "https://www.youtube.com/embed/xveWHTbZ2_o?autoplay=1&mute=0&start=238&end=248;rel=0"],
    ["vivacity", "https://www.youtube.com/embed/aV-5NXwo19o?autoplay=1&mute=0&start=804&end=814;rel=0"],
    ["greed", "https://www.youtube.com/embed/qZjr2CIEflc?autoplay=1&mute=0&start=340&end=350;rel=0"],
    ["stroll", "https://www.youtube.com/embed/7xeFP0SEDdc?autoplay=1&mute=0&start=2414&end=2424;rel=0"],
    ["exacerbate", "https://www.youtube.com/embed/15-DE4i30m8?autoplay=1&mute=0&start=445&end=455;rel=0"],
    ["prosperity", "https://www.youtube.com/embed/87AEeLpodnE?autoplay=1&mute=0&start=759&end=769;rel=0"]
]

class ShowMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.webview = QWebEngineView()
        self.profile = QWebEngineProfile("my_profile", self.webview)
        self.profile.defaultProfile().setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        self.webpage = QWebEnginePage(self.profile, self.webview)
        self.webpage.settings().setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)

        self.webview.setPage(self.webpage)
        self.webview.load(QUrl(words[0][1]))
        self.webview.show()

        self.word_num = 1
        self._updator = QTimer(self)
        self._updator.setSingleShot(False)
        self._updator.timeout.connect(self.reload_next)

        self._updator.start(8000)

    def reload_next(self):
        self.word_num += 1
        if self.word_num >= len(words):
            self._updator.stop()

        self.webview.load(QUrl(words[self.word_num][1]))
        self.webview.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    LiveGraph = ShowMainWindow()

    sys.exit(app.exec_())










