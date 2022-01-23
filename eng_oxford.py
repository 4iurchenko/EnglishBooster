import requests
import json

class GetWord():
    def __init__(self, word, language = "en-gb"):
        with open('secret_oxford.json') as f:
            oxford_secret = json.load(f)
            self.app_id = oxford_secret["app_id"]
            self.app_key = oxford_secret["app_key"]

        self.language = language
        self.word = word

        self.url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + self.language + "/" + self.word.lower()
        self.r = requests.get(self.url, headers={"app_id": self.app_id, "app_key": self.app_key})

        self.answer_json = self.r.json()

    def getAnswerJson(self):
        return self.answer_json

    def getDefinition(self):
        try:
            definition = self.answer_json["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
            return definition
        except:
            return ""


    def getExample(self):
        try:
            examples = self.answer_json["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"]
            return examples
        except:
            return ""

    def getSynonyms(self):
        try:
            synonyms = [x["text"] for x in self.answer_json["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["synonyms"]]
            return synonyms
        except:
            return []

words = [
    ["poverty", "https://www.youtube.com/embed/15-DE4i30m8?autoplay=1&mute=0&start=202&end=212;rel=0"]
]
"""
for i in words:
    word = i[0]
    j = GetWord(word)
    print("-------->>>Word: ", word)
    print("Definition: ", j.getDefinition())
    print("Example: ", j.getExample())
    print("Synonyms :", j.getSynonyms())
"""

