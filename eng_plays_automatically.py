"""
list of 10 words: word, youtubelink, time start
Player plays all the words, 10 seconds, automatically to the end

"""


from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt5.QtWidgets import QApplication
import time

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    webview = QWebEngineView()
    profile = QWebEngineProfile("my_profile", webview)
    profile.defaultProfile().setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
    webpage = QWebEnginePage(profile, webview)
    webpage.settings().setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)

    webview.setPage(webpage)
    webview.load(QUrl("https://www.youtube.com/embed/15-DE4i30m8?autoplay=1&mute=0&start=624&end=628;rel=0"))
    webview.show()

    webview.load(QUrl("https://www.youtube.com/embed/LTOWDhA_I9U?autoplay=1&mute=0&start=65&end=69;rel=0"))
    webview.show()

    sys.exit(app.exec_())




