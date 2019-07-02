import json
from tornado import ioloop, httpclient

json_pages = {}

threads = 300

i = 0

# use a library that helps build graphql statements

headers = {"Content-Type":"application/json",
                   "Origin":"https://anichart.net",
                   "Referer":"https://anichart.net/e8210097149260262919.worker.js",
                   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}

def get_data(last_page):
    global threads
    http_client = httpclient.AsyncHTTPClient(force_instance=True,defaults=dict(user_agent="Mozilla/5.0"),max_clients=threads)
    for page in range(1,last_page+1):
        global i
        i += 1
        url = "https://graphql.anilist.co/"

        headers = {"Content-Type":"application/json",
                   "Origin":"https://anichart.net",
                   "Referer":"https://anichart.net/e8210097149260262919.worker.js",
                   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}

        variables = {"page":page}

        # Improve query readability (use a multiline string and figure out a way to not be against the far left) and also allow the use of cli arguments to request different data (season, year, show type, etc)
        # consider storing the query inside an external file,
        # also consider breaking it up over multiple variables or even a dictionary/json data struct

        query_response_format = "{\n\tPage(page: $page) {\n\t\tpageInfo {\n\t\t\thasNextPage\n\t\t\ttotal\n\t\tperPage\n\t\tcurrentPage\n\t\tlastPage\n\t\t}\n\t\tmedia(\n\t\t\tsort: ID,\n\t\t) {\n\t\t\t\nid\nidMal\ntitle {\n\tromaji\n\tnative\n\tenglish\n}\nstartDate {\n\tyear\n\tmonth\n\tday\n}\nendDate {\n\tyear\n\tmonth\n\tday\n}\nstatus\nseason\nformat\ngenres\nsynonyms\nduration\npopularity\nepisodes\nsource(version: 2)\ncountryOfOrigin\nhashtag\naverageScore\nsiteUrl\ndescription\nbannerImage\nisAdult\ncoverImage {\n\textraLarge\n\tcolor\n}\ntrailer {\n\tid\n\tsite\n\tthumbnail\n}\nexternalLinks {\n\tsite\n\turl\n}\nrankings {\n\trank\n\ttype\n\tseason\n\tallTime\n}\nstudios(isMain: true) {\n\tnodes {\n\t\tid\n\t\tname\n\t\tsiteUrl\n\t}\n}\nrelations {\n\tedges {\n\t\trelationType(version: 2)\n\t\tnode {\n\t\t\tid\n\t\t\ttitle {\n\t\t\t\tromaji\n\t\t\t\tnative\n\t\t\t\tenglish\n\t\t\t}\n\t\t\tsiteUrl\n\t\t}\n\t}\n}\n\nairingSchedule(\n\tnotYetAired: true\n\tperPage: 2\n) {\n\tnodes {\n\t\tepisode\n\t\tairingAt\n\t}\n}\n\n\t\t}\n\t}\n}"
        query = "query (\n\t$page: Int,\n)"+query_response_format
        json_data = {"query":query,
                "variables":variables}
        body = json.dumps(json_data)
        
        http_client.fetch(url.strip(),page_response_handler, method='POST', headers=headers, body=body,connect_timeout=10000,request_timeout=10000)
    ioloop.IOLoop.instance().start()


def page_response_handler(response):
    global headers
    if response.code == 599:
        print(response.effective_url)
        data = response.get_argument('data', 'no data recieved') #maybe body
        http_client.fetch(response.effective_url.strip(), page_response_handler, method='POST', headers=headers, body=data,connect_timeout=10000,request_timeout=10000)
    else:
        global i, json_pages
        i -= 1
        html = response.body.decode('utf-8')
        url = response.effective_url
        time = response.request_time

        rem_req = response.headers['X-RateLimit-Remaining']
        
        json_data = json.loads(html)

        res_data = json_data['data']
        next_page = res_data['Page']['pageInfo']['hasNextPage']
        page_data = res_data['Page']['media']
        last_page = res_data['Page']['pageInfo']['lastPage']
        current_page = res_data['Page']['pageInfo']['currentPage']

        json_pages[current_page] = page_data

        print(f"{round((len(json_pages)/last_page)*100, 2)}%")
            
        if i == 0:
            ioloop.IOLoop.instance().stop()
            save_data()

def get_page_amount():
    try:
        
        url = "https://graphql.anilist.co/"

        headers = {"Content-Type":"application/json",
                   "Origin":"https://anichart.net",
                   "Referer":"https://anichart.net/e8210097149260262919.worker.js",
                   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}

        variables = {"page":1}

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
            last_page = res_data['Page']['pageInfo']['lastPage']
        
    except Exception as e:
        print(e)
        next_page = download_data(page_num)

    return last_page

def save_data():
    global json_pages,pages
    print("Processing Data...")
    final_json = '['+",".join([json.dumps(json_page)[1:-1] for json_page in [json_pages[i] for i in range(1, pages+1)]])+']' #iterates through the dictionary to create a sorted list, turns each individual page in the list into a string, trims the excess containers and combines it with all other entries, seperated only by comma
    print("Saving Data...")
    with open("database.json", "w") as file:
        file.write(final_json)
    print("Saved.")

pages = get_page_amount()

print(f"Pages: {pages}")

get_data(pages)
