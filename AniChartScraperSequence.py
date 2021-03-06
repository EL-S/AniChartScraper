import requests
import json

json_pages = []

# add threading back in, determine how many pages there is using an algorithm perhaps
# attempt to request all data through graphql, eg. anti-pagination 


def download_data(page_num):
    try:
        global json_pages
        
        url = "https://graphql.anilist.co/"

        headers = {"Content-Type":"application/json",
                   "Origin":"https://anichart.net",
                   "Referer":"https://anichart.net/e8210097149260262919.worker.js",
                   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}

        variables = {"page":int(page_num)}

        query_response_format = "{\n\tPage(page: $page) {\n\t\tpageInfo {\n\t\t\thasNextPage\n\t\t\ttotal\n\t\tperPage\n\t\tcurrentPage\n\t\tlastPage\n\t\t}\n\t\tmedia(\n\t\t\tsort: TITLE_ROMAJI,\n\t\t) {\n\t\t\t\nid\nidMal\ntitle {\n\tromaji\n\tnative\n\tenglish\n}\nstartDate {\n\tyear\n\tmonth\n\tday\n}\nendDate {\n\tyear\n\tmonth\n\tday\n}\nstatus\nseason\nformat\ngenres\nsynonyms\nduration\npopularity\nepisodes\nsource(version: 2)\ncountryOfOrigin\nhashtag\naverageScore\nsiteUrl\ndescription\nbannerImage\nisAdult\ncoverImage {\n\textraLarge\n\tcolor\n}\ntrailer {\n\tid\n\tsite\n\tthumbnail\n}\nexternalLinks {\n\tsite\n\turl\n}\nrankings {\n\trank\n\ttype\n\tseason\n\tallTime\n}\nstudios(isMain: true) {\n\tnodes {\n\t\tid\n\t\tname\n\t\tsiteUrl\n\t}\n}\nrelations {\n\tedges {\n\t\trelationType(version: 2)\n\t\tnode {\n\t\t\tid\n\t\t\ttitle {\n\t\t\t\tromaji\n\t\t\t\tnative\n\t\t\t\tenglish\n\t\t\t}\n\t\t\tsiteUrl\n\t\t}\n\t}\n}\n\nairingSchedule(\n\tnotYetAired: true\n\tperPage: 2\n) {\n\tnodes {\n\t\tepisode\n\t\tairingAt\n\t}\n}\n\n\t\t}\n\t}\n}"
        query = "query (\n\t$page: Int,\n)"+query_response_format
        json_data = {"query":query,
                "variables":variables}

        res = requests.post(url, headers=headers, json=json_data)

        if res.status_code != 200:
            raise requests.HTTPError('Reattempting page...')
        else:
            rem_req = res.headers['X-RateLimit-Remaining']
            
            res_data_raw = res.text

            json_str = json.loads(res_data_raw)
            res_data = json_str['data']
            next_page = res_data['Page']['pageInfo']['hasNextPage']
            page_data = res_data['Page']['media']
            last_page = res_data['Page']['pageInfo']['lastPage']
            current_page = res_data['Page']['pageInfo']['currentPage']
            
            print(f"Remaining Requests Allowed: {rem_req}\nPage: {page_num}, Remaining: {last_page-current_page}")
            
            json_pages.append(page_data)
        
    except Exception as e:
        print(e)
        next_page = download_data(page_num)

    return next_page

page = 1

next_page = download_data(page)

while next_page == True:
    if next_page == True: #yes a string
        page += 1
        next_page = download_data(page)

final_json = '['+",".join([json.dumps(json_page)[1:-1] for json_page in json_pages])+']' #turns each individual page into a string, trims the excess containers and combines it with all other entries, seperated only by comma

with open("database.json", "w") as file:
    file.write(final_json)
