import os
import json

file_name = "data.csv"
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

with open("database.json", "r") as file:
    json_str = file.read()

result = json.loads(json_str)
for anime in result:
    if silent != True
        print(anime['id'],anime['title_english'],anime['title_romaji'])
    anime_id = anime['id']
    title_english = anime['title_english']
    title_romaji = anime['title_romaji']
    rating = anime['average_score']
    popularity = anime['popularity']
    data = (str(anime_id),str(title_english),str(title_romaji),str(rating),str(popularity))
    data_line = ",".join(data)
    with open(full_path, "a", encoding="utf-8") as data_csv:
        data_csv.write(data_line+"\n")
