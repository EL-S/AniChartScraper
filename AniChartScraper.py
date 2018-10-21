from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import sys
import json

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

url =  "http://anichart.net/api/browse/anime?season=Fall&year=2018&sort=title_romaji&full_page=true&airing_data=true&page=1"

cookie = {'XSRF-TOKEN': 'ILfjB7FSaQF0mXdKUTVtyPuY9UAgXespt3xOFTu5'}
request = Request(url)
request.add_header('Host','anichart.net')
request.add_header('Connection','keep-alive')
request.add_header('Accept','application/json, text/plain, */*')
request.add_header('X-CSRF-TOKEN','ILfjB7FSaQF0mXdKUTVtyPuY9UAgXespt3xOFTu5')
request.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
request.add_header('Referer','http://anichart.net/Fall-2018')
request.add_header('Accept-Encoding','gzip, deflate')
request.add_header('Accept-Language','en-US,en;q=0.9')
request.add_header('Cookie','XSRF-TOKEN=ILfjB7FSaQF0mXdKUTVtyPuY9UAgXespt3xOFTu5; laravel_session=eyJpdiI6ImNTZ1ZaYnRiTit0VU1GNjA5OXVhWmc9PSIsInZhbHVlIjoiUnpDbktPRmtScmlVRTJ0SE9scVRENGxaTTd1REZjR3F3TzNMYWJEenR5REZKbEpcL2VtVm1XQzNDV1I0RDdrNVp0ZE1nc0xuYVBhMTNrV1ZBRXRZa1l3PT0iLCJtYWMiOiI2YzVkNmU0YzcxZjA4YzMwZDY5NjFjMDJiZjdlYjRiMDgxMjhjZGYyMzIyZGI5OGMxYmJmMzAwZDJmZGY3NTczIn0%3D')
page = urlopen(request)
print(page.read().decode("ISO 8859-16"))
result = json.loads(page.read().decode("gzip"))
print(result)
soup = BeautifulSoup(page, 'html.parser')

div = soup.findAll('div')
anime_divs = div.findAll("div", attrs={"class":"card"})
for element in anime_divs:
    print(element.find("div", attrs={"class":"title"}).find("a").strip())
#<div class="section" ng-repeat="(section, series) in browseVm.b" dom-ready="">
