from urllib.request import Request, urlopen
import json
import gzip

for page_num in range(275,280):
    #page 1-276
    url =  "http://anichart.net/api/browse/anime?page="+str(page_num)

    x_csrf_token = 'Ypc5THqTHYT3oHJ3QOQ9LGULif15NmeBmDiK0Xo5'
    laravel_session = 'eyJpdiI6InBYaXA4cWNnV1JvR01pc1wvZEgxK2hRPT0iLCJ2YWx1ZSI6IktHY3B1OEFBUWIzdWlGY2pXWlpQMThyVG8reVcxSlR3T1pSTVpjV0t2THZKd3hWY2M4enNPNTMzUms5XC9CNlwveStcL1hLVTgxbGRIUkRhTzhsMmVuQU13PT0iLCJtYWMiOiIwOWEzZjk5ZTY5OGJkZGE5YzYxYjA4ZTNmMWRjOGJjZjEyMTExNDkwYTU2YmUxMjYwYWEwMzFjNTljMGEyN2Q1In0%3D'
    request = Request(url,headers={'Host':'anichart.net','Connection':'keep-alive','Accept':'application/json; charset=utf-8','Content-Type':'application/json; charset=utf-8','X-CSRF-TOKEN':x_csrf_token,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','Referer':'http://anichart.net/Fall-2018','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.9','Cookie':'XSRF-TOKEN='+ x_csrf_token+'; laravel_session='+laravel_session})
    page = urlopen(request).read()

    try:
        r = gzip.decompress(page)
    except OSError:
        pass

    json_str = r.decode()

    with open("json.txt", "a") as file:
        file.write(json_str)

    result = json.loads(json_str)

    for i in result:
        print(i['id'],i['title_english'])
