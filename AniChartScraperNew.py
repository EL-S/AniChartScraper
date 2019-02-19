import requests
import json

total_json = []

def download_data(page_num):
    global total_json
    
    url = "https://graphql.anilist.co/"

    headers = {"Content-Type":"application/json",
               "Origin":"https://anichart.net",
               "Referer":"https://anichart.net/e8210097149260262919.worker.js",
               "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}

    variables = {"page":int(page_num)}

    query_respons_format = "{\n\tPage(page: $page) {\n\t\tpageInfo {\n\t\t\thasNextPage\n\t\t\ttotal\n\t\t}\n\t\tmedia(\n\t\t\tformat_not: $excludeFormat,\n\t\t\tstatus: $status,\n\t\t\tepisodes_greater: $minEpisodes,\n\t\t\tisAdult: false,\n\t\t\ttype: ANIME,\n\t\t\tsort: TITLE_ROMAJI,\n\t\t) {\n\t\t\t\nid\nidMal\ntitle {\n\tromaji\n\tnative\n\tenglish\n}\nstartDate {\n\tyear\n\tmonth\n\tday\n}\nendDate {\n\tyear\n\tmonth\n\tday\n}\nstatus\nseason\nformat\ngenres\nsynonyms\nduration\npopularity\nepisodes\nsource(version: 2)\ncountryOfOrigin\nhashtag\naverageScore\nsiteUrl\ndescription\nbannerImage\nisAdult\ncoverImage {\n\textraLarge\n\tcolor\n}\ntrailer {\n\tid\n\tsite\n\tthumbnail\n}\nexternalLinks {\n\tsite\n\turl\n}\nrankings {\n\trank\n\ttype\n\tseason\n\tallTime\n}\nstudios(isMain: true) {\n\tnodes {\n\t\tid\n\t\tname\n\t\tsiteUrl\n\t}\n}\nrelations {\n\tedges {\n\t\trelationType(version: 2)\n\t\tnode {\n\t\t\tid\n\t\t\ttitle {\n\t\t\t\tromaji\n\t\t\t\tnative\n\t\t\t\tenglish\n\t\t\t}\n\t\t\tsiteUrl\n\t\t}\n\t}\n}\n\nairingSchedule(\n\tnotYetAired: true\n\tperPage: 2\n) {\n\tnodes {\n\t\tepisode\n\t\tairingAt\n\t}\n}\n\n\t\t}\n\t}\n}"
    query = "query (\n\t$excludeFormat: MediaFormat,\n\t$status: MediaStatus,\n\t$minEpisodes: Int,\n\t$page: Int,\n)"+query_respons_format
    json_data = {"query":query,
            "variables":variables}

    res = requests.post(url, headers=headers, json=json_data)

    print(res)
    print(res.headers)

    res_data_raw = res.text

    json_str = json.loads(res_data_raw)
    res_data = json_str['data']

    next_page = res_data['Page']['pageInfo']['hasNextPage']
    print(next_page)
    non_dumped_data = res_data['Page']['media']
    json_data_dump = json.dumps(non_dumped_data)
    
    total_json.append(non_dumped_data)
    
    with open("data_bulk_ALL2_"+str(page_num)+".json", "w") as file:
        file.write(json_data_dump)
    
    return next_page

format_var = "TV"
page = 1

#seasons = ["FALL","WINTER","SPRING","SUMMER"]

next_page = download_data(page)
while next_page == True:
    if next_page == True: #yes a string
        page += 1
        next_page = download_data(page)
page = 1

elements = []

for element in total_json:
    element2 = json.dumps(element)
    element3 = element2[1:]
    element4 = element3[:-1]
    elements.append(element4)

final_json = '{"media": ['+",".join(elements)+']}'

with open("database.json", "w") as file:
    file.write(final_json)

#pages = download_data(season,year,format_var,page)
#for page_num in range(2,pages+1): #nup
#    download_data(season,year,format_var,page_num)

