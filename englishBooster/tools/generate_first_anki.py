import random
import json
filename = "../databases/youtube_words_1.txt"
anki_file = "../logs/anki.csv"

app_config = {}
app_config["cnt_study_words"] = 200
app_config["start_before_sec"] = 4
app_config["end_after_sec"] = 2

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
    #result["url"] = "https://www.youtube.com/embed/{vid}?autoplay=1&mute=0&start={start}&end={end};rel=0".format(vid = random_video["vid"], start = int(random_video["start"])-app_config["start_before_sec"], end = int(random_video["end"])+app_config["end_after_sec"])
    result["url"] = """word:<br><iframe width="705" height="321" src="https://www.youtube.com/embed/{vid}?start={start}&end={end}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe>""".format(vid = random_video["vid"], start = int(random_video["start"])-app_config["start_before_sec"], end = int(random_video["end"])+app_config["end_after_sec"])
    list_words.append(result)

print("url"+","+"word")
for i in list_words:
    print(i["url"]+","+i["word"])

with open(anki_file, "w") as f:
    print("url" + "\t" + "word"+'\n')
    for i in list_words:
        print(i["url"] + "\t" + i["word"])
        f.write(i["url"] + "," + i["word"]+'\n')



