__version__ = 'v0.1'
__author__ = 'Yurri'

#import os
import sys
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
import random
import json
filename = "databases/youtube_words_1.txt"
log_file = "logs/listen_write.log"

app_config = {}
app_config["cnt_study_words"] = 3
app_config["vid_duration"] = 13000
app_config["start_before_sec"] = 5
app_config["end_after_sec"] = 5
app_config["is_word_shown"] = 0

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

decorator_gen_data = []
for i in list_words:
    j = {}
    j["word"] = i["word"]
    j["url"] = i["url"]
    j["phrase"] = i["phrase"]
    decorator_gen_data.append(j)

#print(decorator_gen_data)
#print(len(decorator_gen_data))
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

clearConsole()



class YouTubePlayer(QWidget):
    def __init__(self):
        super().__init__()

        defaultSettings = QWebEngineSettings.globalSettings()
        defaultSettings.setFontSize(QWebEngineSettings.MinimumFontSize, 28)

        self.correct_words = []
        self.incorrect_words = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        topLayout = QHBoxLayout()
        self.layout.addLayout(topLayout)

        self.gen_data = decorator_gen_data
        self.word_num = 0

        self.video_duration = app_config["vid_duration"]

        buttonAddPlayer = QPushButton('&Next..', clicked=self.reload_next)
        self.layout.addWidget(buttonAddPlayer)

        label_A = QLabel('Enter a correct word')
        self.input_A = QLineEdit()
        self.input_A.installEventFilter(self)
        #self.input_A.setText(self.gen_data[0]["word"])

        topLayout.addWidget(label_A, 1)
        topLayout.addWidget(self.input_A, 9)

        label_B = QLabel('Feedback')
        self.input_B = QLineEdit()
        self.input_B.installEventFilter(self)
        #self.input_B.setText(self.gen_data[0]["word"])

        topLayout.addWidget(label_B, 1)
        topLayout.addWidget(self.input_B, 9)

        label_C = QLabel('Hint')
        self.input_C = QLineEdit()
        self.input_C.installEventFilter(self)
        if (app_config["is_word_shown"]==1):
            self.input_C.setText(self.gen_data[0]["word"])

        topLayout.addWidget(label_C, 1)
        topLayout.addWidget(self.input_C, 9)

        self.webview = self.addWebView(url=self.gen_data[0]["url"])

        buttonLayout = QHBoxLayout()
        self.layout.addLayout(buttonLayout)
        print(self.word_num)

    def reload_next(self):
        self.word_num += 1 #iterate to the next word

        #adding statistic
        if (self.input_A.text() == self.gen_data[self.word_num-1]["word"]):
            self.input_B.setText("+")
            self.correct_words.append(self.gen_data[self.word_num-1]["word"]) #add + words to the account
        else:
            self.input_B.setText("..")
            self.incorrect_words.append(self.gen_data[self.word_num-1]["word"]) #add - words to the account

        if self.word_num == len(self.gen_data):
            self.writeResults()
            sys.exit(app.exec_())

        if self.word_num == len(self.gen_data)-1:
            self.input_C.setText("It is the last word in a queue:)")

        self.input_A.setText("") #clear input

        if (app_config["is_word_shown"] == 1):
            self.input_C.setText(self.gen_data[self.word_num]["word"]) #sets current word as a hint

        url = self.gen_data[self.word_num]["url"]
        self.webview.load(QUrl(url))
        self.webview.show()

    def writeResults(self):
        percentage_correct = str(
            int(100 * len(self.correct_words) / (len(self.correct_words) + len(self.incorrect_words))))
        text_correct_words = ", ".join(self.correct_words)
        text_incorrect_words = ", ".join(self.incorrect_words)

        with open(log_file, "a") as f:
            f.write('\n')
            f.write("\nBest words are " + text_correct_words)
            f.write("\nMistakes are in " + text_incorrect_words)
            f.write("\nFinal result of right answers is " + percentage_correct)

            print("\nBest words are " + text_correct_words)
            print("\nMistakes are in " + text_incorrect_words)
            print("\nFinal result of right answers is " + percentage_correct)

        print("Log file with the results updated")

    def addWebView(self, url):
        self.webview = QWebEngineView()
        self.profile = QWebEngineProfile("my_profile", self.webview)
        self.profile.defaultProfile().setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        self.webpage = QWebEnginePage(self.profile, self.webview)
        self.webpage.settings().setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)

        self.webview.setPage(self.webpage)
        self.webview.load(QUrl(url))
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






