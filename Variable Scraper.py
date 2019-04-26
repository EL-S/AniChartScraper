import requests
import json

def download_data(season,year,format_var,page_num):
    url = "https://graphql.anilist.co/"

    headers = {"Content-Type":"application/json",
               "Origin":"https://anichart.net",
               "Referer":"https://anichart.net/e8210097149260262919.worker.js",
               "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}

    variables = {"season":season,
                 "year":year,
                 "format":format_var,
                 "page":int(page_num)}

    query_respons_format = "{\n\tPage(page: $page) {\n\t\tpageInfo {\n\t\t\thasNextPage\n\t\t\ttotal\n\t\t}\n\t\tmedia(\n\t\t\tseason: $season\n\t\t\tseasonYear: $year\n\t\t\tformat: $format,\n\t\t\tformat_not: $excludeFormat,\n\t\t\tstatus: $status,\n\t\t\tepisodes_greater: $minEpisodes,\n\t\t\tisAdult: false,\n\t\t\ttype: ANIME,\n\t\t\tsort: TITLE_ROMAJI,\n\t\t) {\n\t\t\t\nid\nidMal\ntitle {\n\tromaji\n\tnative\n\tenglish\n}\nstartDate {\n\tyear\n\tmonth\n\tday\n}\nendDate {\n\tyear\n\tmonth\n\tday\n}\nstatus\nseason\nformat\ngenres\nsynonyms\nduration\npopularity\nepisodes\nsource(version: 2)\ncountryOfOrigin\nhashtag\naverageScore\nsiteUrl\ndescription\nbannerImage\nisAdult\ncoverImage {\n\textraLarge\n\tcolor\n}\ntrailer {\n\tid\n\tsite\n\tthumbnail\n}\nexternalLinks {\n\tsite\n\turl\n}\nrankings {\n\trank\n\ttype\n\tseason\n\tallTime\n}\nstudios(isMain: true) {\n\tnodes {\n\t\tid\n\t\tname\n\t\tsiteUrl\n\t}\n}\nrelations {\n\tedges {\n\t\trelationType(version: 2)\n\t\tnode {\n\t\t\tid\n\t\t\ttitle {\n\t\t\t\tromaji\n\t\t\t\tnative\n\t\t\t\tenglish\n\t\t\t}\n\t\t\tsiteUrl\n\t\t}\n\t}\n}\n\nairingSchedule(\n\tnotYetAired: true\n\tperPage: 2\n) {\n\tnodes {\n\t\tepisode\n\t\tairingAt\n\t}\n}\n\n\t\t}\n\t}\n}"
    query = "query (\n\t$season: MediaSeason,\n\t$year: Int,\n\t$format: MediaFormat,\n\t$excludeFormat: MediaFormat,\n\t$status: MediaStatus,\n\t$minEpisodes: Int,\n\t$page: Int,\n)"+query_respons_format
    json_data = {"query":query,
            "variables":variables}

    res = requests.post(url, headers=headers, json=json_data)

    print(res)
    print(res.headers)

    res_data_raw = res.text

    json_str = json.loads(res_data_raw)
    res_data = json_str['data']

    next_page = res_data['Page']['pageInfo']['hasNextPage']

    json_data_dump = json.dumps(res_data)

    with open("data_"+str(year)+"_"+str(season)+"_"+str(format_var)+"_"+str(page_num)+".json", "w") as file:
        file.write(json_data_dump)

    return next_page

#season = "FALL"
#year = 2017
format_var = "TV"
page = 1

seasons = ["FALL","WINTER","SPRING","SUMMER"]

for year in range(1973,2025):
    for season in seasons:
        next_page = download_data(season,year,format_var,page)
        while next_page == True:
            if next_page == True: #yes a string
                page += 1
                next_page = download_data(season,year,format_var,page_num)

#pages = download_data(season,year,format_var,page)
#for page_num in range(2,pages+1): #nup
#    download_data(season,year,format_var,page_num)

