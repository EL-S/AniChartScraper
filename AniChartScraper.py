from urllib.request import Request, urlopen
import json
import gzip
import os

#page 1-276
start = 1
end = 276
name = "database"
extension = ".json"
filename = name+extension
silent = True

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
            for i in values:
                try:
                    cookies[i.split("=")[0].strip()] = i.split("=")[1].strip()
                except:
                    cookies[i.strip()] = "Unknown"

get_token()
check_file()

for page_num in range(start,end+1):
    print("Page:",page_num)
    url =  "http://anichart.net/api/browse/anime?page="+str(page_num)

    x_csrf_token = cookies['XSRF-TOKEN']
    laravel_session = cookies['laravel_session']
    request = Request(url,headers={'Host':'anichart.net','Connection':'keep-alive','Accept':'application/json; charset=utf-8','Content-Type':'application/json; charset=utf-8','X-CSRF-TOKEN':x_csrf_token,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Referer':'http://anichart.net/Fall-2018','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cookie':'XSRF-TOKEN='+ x_csrf_token+'; laravel_session='+laravel_session})
    page = urlopen(request).read()

    try:
        r = gzip.decompress(page)
    except OSError:
        pass

    json_str = r.decode()

    with open(filename, "a") as file:
        if page_num == start:
            file.write(json_str[:-1]+str(","))
        elif page_num == end:
            file.write(json_str[1:])
        else:
            file.write(json_str[1:-1]+str(","))

    result = json.loads(json_str)
    if not silent:
        for i in result:
            print(i['id'],i['title_english'])
