import os
import json

file_name = "analysis.csv"
directory = "data/"
full_path = directory + file_name
silent = True

def check_file():
    global full_path,directory
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    try:
        os.remove(full_path)
        print("File removed to prevent conflicts!")
    except:
        pass
    try:
        with open(full_path, "w") as file:
            file.write("")
    except:
        pass
    
check_file()

lines = []

with open("database.json", "r") as file:
    json_str = file.read()

result = json.loads(json_str)
for anime in result:
    title = anime['title']
    if silent != True:
        try:
            title_romaji = title['romaji']
        except:
            title_romaji = ""
        try:
            title_english = title['english']
        except:
            title_english = ""
        print(anime['id'],title_english,title_romaji)
    try:
        anime_id = anime['idMal']
    except:
        anime_id = "-1"
    title_english = title['english']
    mal_link = anime['siteUrl']
    title_romaji = title['romaji']
    rating = anime['averageScore']
    popularity = anime['popularity']
    episodes = anime['episodes']
    data = (str(anime_id),str(title_english),str(title_romaji),str(rating),str(popularity))
    #data = (str(anime_id),str(mal_link))
    data_line = ",".join(data)
    lines.append(data_line)
    
with open(full_path, "w", encoding="utf-8") as data_csv:
    data_csv.write("\n".join(lines))
