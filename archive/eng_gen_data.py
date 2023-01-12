import eng_gsheet as gs
import eng_oxford
import requests
import json
import gspread

def get_config():
    config = gs.EngGoogleSheet(sh_name="To-do list", wks_name="conf")
    d_list = config.getFields(r_from=0, r_to=999)

    vid_duration = 5
    is_show_word = 1
    is_show_synonym = 1

    for i in d_list:
        if (i[0] == "single video duration"):
            vid_duration = int(i[1])

        if (i[0] == "show word"):
            is_show_word = int(i[1])

        if (i[0] == "show synonyms"):
            is_show_synonym = int(i[1])

    vid_duration = vid_duration
    is_show_word = is_show_word
    is_show_synonym = is_show_synonym

    return {"vid_duration": vid_duration,
            "is_show_word": is_show_word,
            "is_show_synonym": is_show_synonym
            }

def gen_data():
    # Creating the list of right url
    words = gs.EngGoogleSheet(sh_name = "To-do list", wks_name = "tifwords3000")
    w_list = words.getFields(r_from = 3, r_to = 999999)
    w_list_filt = [x for x in w_list if (x[0] == "TRUE" and (x[1] != "" or x[2] != "" or x[3] != ""))]

    main_words = []

    for i in w_list_filt:
        word = i[2]
        url = i[4]
        video_id = url[17:28]
        print(i)
        time_start = int(url[31::])
        vid_duration = int(get_config()["vid_duration"])
        time_end = time_start + vid_duration//1000
        new_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=0&start={time_start}&end={time_end};rel=0"

        oxford_w = ""# eng_oxford.GetWord(word)
        synonyms = ""# oxford_w.getSynonyms()
        definition = ""# = oxford_w.getDefinition()
        example = ""# oxford_w.getExample()

        #word, customized_url, list_of_synonyms
        print([word, new_url, synonyms, definition, example])
        main_words.append([word, new_url, synonyms, definition, example])

    return main_words



def get_spreedsheet_data(sh_name = "test_doc", wks_name = "test_wks", zone = "A1:B2"):
    sa = gspread.service_account(filename="../secret_client.json")
    sh = sa.open(sh_name)
    wks = sh.worksheet(wks_name)
    wks_data = wks.batch_get([zone])
    return wks_data
# print(get_spreedsheet_data(sh_name = "To-do list", wks_name = "win800webster", zone = 'A4:B403'))

def fit_sublists_to_size(list = [[], []], size = 2, filler = ''):
    l = len(list)
    for i in range(0, l):
        list[i] = list[i] + [filler] * (size - len(list[i]))
    return list
# print(fit_sublists_to_size(list = [[1, 2, 3], [1, 2]], size = 3, filler = 'XXX'))

def get_youtube_url(short_url = "https://youtu.be/WSKPrVG3Evs?t=821", vid_duration = 10000):
    video_id = short_url[17:28]
    time_start = int(short_url[31::])
    #vid_duration = int(get_config()["vid_duration"])
    time_end = time_start + vid_duration // 1000
    long_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=0&start={time_start}&end={time_end};rel=0"
    return long_url



