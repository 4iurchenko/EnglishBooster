__version__ = 'v1.1'
__author__ = 'Iurii'

#import os
import sys
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
import random
import json
filename = "databases/youtube_words_1.txt"

app_config = {}
app_config["cnt_study_words"] = 6
app_config["vid_duration"] = 13000
app_config["start_before_sec"] = 5
app_config["end_after_sec"] = 5

list_words = []
with open(filename, 'r') as file1:
    lines = file1.readlines()

random_list = random.sample(range(0, len(lines)), app_config["cnt_study_words"])

for i in random_list:
    random_word = json.loads(lines[i])
    word = random_word['word']
    word_results = random_word['results']
    random_video = word_results[random.randint(0, len(word_results)-1)]

    result = {}
    result["word"] = word
    result["phrase"] = random_video["display"]
    result["vid"] = random_video["vid"]
    result["start"] = random_video["start"]
    result["end"] = random_video["end"]
    result["url"] = "https://www.youtube.com/embed/{vid}?autoplay=1&mute=0&start={start}&end={end};rel=0".format(vid = random_video["vid"], start = int(random_video["start"])-app_config["start_before_sec"], end = int(random_video["end"])+app_config["end_after_sec"])
    list_words.append(result)

print(list_words)

decorator_gen_data = []
for i in list_words:
    j = []
    j.append(i["word"])  #word
    j.append(i["url"]) #url
    j.append(i["phrase"]) #synonym
    j.append(i["word"]) #definition
    j.append("") #example

    decorator_gen_data.append(j)

print(decorator_gen_data)
print(len(decorator_gen_data))




class YouTubePlayer(QWidget):
    def __init__(self):
        super().__init__()

        defaultSettings = QWebEngineSettings.globalSettings()
        defaultSettings.setFontSize(QWebEngineSettings.MinimumFontSize, 28)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        topLayout = QHBoxLayout()
        self.layout.addLayout(topLayout)

        self.gen_data = decorator_gen_data
        self.word_num = 0

        self.video_duration = app_config["vid_duration"]

        buttonAddPlayer = QPushButton('&Your language will be IELTS 8.0', clicked=self.restartVideo)
        self.layout.addWidget(buttonAddPlayer)

        label_synonyms = QLabel('S: ')
        self.input_synonyms = QLineEdit()
        self.input_synonyms.installEventFilter(self)
        self.input_synonyms.setText(self.gen_data[0][2])

        topLayout.addWidget(label_synonyms, 1)
        topLayout.addWidget(self.input_synonyms, 9)

        label_definition = QLabel('D: ')
        self.input_definition = QLineEdit()
        self.input_definition.installEventFilter(self)
        self.input_definition.setText(self.gen_data[0][3])

        topLayout.addWidget(label_definition, 1)
        topLayout.addWidget(self.input_definition, 9)

        label_example = QLabel('Ex: ')
        self.input_example = QLineEdit()
        self.input_example.installEventFilter(self)
        self.input_example.setText(self.gen_data[0][4])

        topLayout.addWidget(label_example, 1)
        topLayout.addWidget(self.input_example, 9)

        self.webview = self.addWebView()

        buttonLayout = QHBoxLayout()
        self.layout.addLayout(buttonLayout)


        self._updator = QTimer(self)
        self._updator.setSingleShot(False)
        self._updator.timeout.connect(self.reload_next)

        self._updator.start(self.video_duration)


    def restartVideo(self):
        #self.word_num += 1
        #self.input_synonyms.setText(str(self.word_num))

        self.word_num = 0
        self._updator = QTimer(self)
        self._updator.setSingleShot(False)
        self._updator.timeout.connect(self.reload_next)
        self._updator.start(self.video_duration)


    def reload_next(self):
        if self.word_num < len(self.gen_data)-1:
            self.word_num += 1
            url = self.gen_data[self.word_num][1]
            self.webview.load(QUrl(url))
            self.webview.show()

            self.input_synonyms.setText(self.gen_data[self.word_num][2])
            self.input_definition.setText(self.gen_data[self.word_num][3])
            self.input_example.setText(self.gen_data[self.word_num][4])
            return 0
        else:
            self._updator.stop()
            self._updator.disconnect()
            return 1

    def addWebView(self):
        self.webview = QWebEngineView()
        self.profile = QWebEngineProfile("my_profile", self.webview)
        self.profile.defaultProfile().setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        self.webpage = QWebEnginePage(self.profile, self.webview)
        self.webpage.settings().setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)

        self.webview.setPage(self.webpage)
        self.webview.load(QUrl(self.gen_data[0][1]))
        self.layout.addWidget(self.webview)
        return self.webview


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Player")
        self.setMinimumSize(800, 400)
        self.players = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.videoGrid = QGridLayout()
        self.layout.addLayout(self.videoGrid)

        self.player = YouTubePlayer()
        self.videoGrid.addWidget(self.player, 0, 0)

        self.layout.addWidget(QLabel(__version__ + ' by ' + __author__), alignment=Qt.AlignBottom | Qt.AlignRight)

        self.setStyleSheet("""
            QPushButton {
                font-size: 28px;
                height: 40px;
                background-color: #E41937;
                color: white;
            }

            * {
                background-color: #83C2FF;
                font-size: 30 px;
            }

            QLineEdit {
                background-color: white;
                color: black;
            }    
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Player Window Closed')

    sys.exit(app.exec_())






