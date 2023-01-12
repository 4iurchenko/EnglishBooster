import requests
import json
import gspread
sh_name = "To-do list"
wks_name = "new_portion"

sa = gspread.service_account(filename="../secret_client.json")
sh = sa.open(sh_name)
wks = sh.worksheet(wks_name)

wks_data = wks.batch_get(['A4:B437'])

print(wks_data)

for i in range(0, len(wks_data[0])):
    word = wks_data[0][i][0]
    print(word)
    url = f"https://www.dictionaryapi.com/api/v3/references/learners/json/{word}?key=b915b321-5c27-4d2a-bbc7-ebe06c237741"

    r = requests.get(url)
    d = r.json()
    shortdef = d[0]["shortdef"]
    wks_data[0][i][1] = "; ".join(shortdef)

print(wks_data[0])


wks.batch_update([{
    'range': 'A4:B437',
    'values': wks_data[0]
}])