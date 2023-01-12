import requests
api_key = "12f39723-4332-4b97-97d9-2ac3f50af6cc"
word = "disposal"
url = f'https://youglish.com/api/v1/videos/search?key={api_key}&query={word}&lg=english&accent=us'
r = requests.get(url)
d = r.json()
for i in d['results']:
    print(i)
    t = i["display"]
    v = i["vid"]
    s = i["start"]
    e = i["end"]
    print(t)
    print(v)
    print(s)
    print(e)
