from urllib.request import Request, urlopen
from tornado import ioloop, httpclient
import json
import gzip
import os

#page 1-276
start = 1
end = 300
name = "database"
extension = ".json"
threads = 20
filename = name+extension
silent = True
i = 0
pages_downloaded = []
pages_json = {}
cookies = {}

def check_file():
    global filename
    try:
        os.remove(filename)
        print("File removed to prevent conflicts!")
    except:
        pass

def get_token(): #poll homepage and obtain a token for each section automatically
    global cookies
    url = "http://anichart.net"
    request = Request(url)
    response = urlopen(request)
    for key,value in response.headers.items():
        if key == "Set-Cookie":
            values = value.split(";")
            for y in values:
                try:
                    cookies[y.split("=")[0].strip()] = y.split("=")[1].strip()
                except:
                    cookies[y.strip()] = "Unknown"

def create_json_file():
    global pages_downloaded, pages_json, filename, silent, start, end
    pages_downloaded.sort(key=int)
    complete_json_str = ""
    flag = False
    
    for page_id in pages_downloaded:
        json_str = pages_json[page_id]
        if page_id == start:
            json_str = json_str[:-1]+str(",") #strip last and don't strip first character
        elif (page_id == end) and (json_str != "[]"): #strip first character
            json_str = json_str[1:]
        elif json_str == "[]" and (flag == False): #if it's blank for the first time
            flag = True #strip the entire jsons last character and close it
            complete_json_str = complete_json_str[:-1]
            json_str = str("]")
            print("Found Empty Page, Finishing")
        elif (flag == False): #strip brackets and add a comma
            json_str = json_str[1:-1]+str(",")
        else: #do not handle, if this runs for some reason
            json_str = ""
        complete_json_str = complete_json_str + json_str
        if (flag == True):
            break
        print("Page:",page_id)
    with open(filename, "w") as file:
        file.write(complete_json_str)
##    result = json.loads(json_str)
##    if not silent:
##        for y in result:
##            print(y['id'],y['title_english'])

def download_json():
    global cookies,start,end,i,threads

    x_csrf_token = cookies['XSRF-TOKEN']
    laravel_session = cookies['laravel_session']
        
    http_client = httpclient.AsyncHTTPClient(force_instance=True,defaults=dict(user_agent="Mozilla/5.0"),max_clients=threads)
    for page_num in range(start,end+1):
        url =  "http://anichart.net/api/browse/anime?page="+str(page_num)
        headers={'Host':'anichart.net','Connection':'keep-alive','Accept':'application/json; charset=utf-8','Content-Type':'application/json; charset=utf-8','X-CSRF-TOKEN':x_csrf_token,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Referer':'http://anichart.net/Fall-2018','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cookie':'XSRF-TOKEN='+ x_csrf_token+'; laravel_session='+laravel_session}
        request = httpclient.HTTPRequest(url.strip(), headers=headers,method='GET',connect_timeout=10000,request_timeout=10000)
        http_client.fetch(request,handle_chapter_response)
        i += 1
    ioloop.IOLoop.instance().start()

def handle_chapter_response(response):
    if response.code == 599:
        print(response.effective_url,"error")
        http_client.fetch(response.effective_url.strip(), handle_chapter_response, method='GET',connect_timeout=10000,request_timeout=10000)
    else:
        global i,pages_downloaded,pages_json
        data = response.body.decode('utf-8') #automatic gzip decompress apparently
        url = response.effective_url
        try:
            print(url)
            page_id = int(url.split("?")[1].split("=")[1])
            #print(page_id)
            pages_downloaded.append(page_id)
            pages_json[page_id] = data
        except Exception as e:
            print(e)
        i -= 1
        if i == 0: #all pages loaded
            ioloop.IOLoop.instance().stop()
            create_json_file()

get_token()
check_file()
download_json()


print("Complete")
        
