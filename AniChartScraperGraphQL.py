import requests
import json
from graphqlclient import GraphQLClient

json_pages = []

# add threading back in, determine how many pages there is using an algorithm perhaps
# attempt to request all data through graphql, eg. anti-pagination 

def download_data(page_num):
    try:
        global json_pages
        
        url = "https://graphql.anilist.co/"

        client = GraphQLClient(url)
        client.inject_token('application/json','Content-Type')
        client.inject_token('https://anichart.net','Origin')
        client.inject_token('https://anichart.net/e8210097149260262919.worker.js','Referer')
        client.inject_token('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36','User-Agent')


        res = client.execute('''
            {
              Page(page: '''+str(page_num)+''') {
                pageInfo {
                  hasNextPage,
                  total,
                  perPage,
                  currentPage,
                  lastPage,
                },
                media {
                  idMal,
                  title {
                    romaji,
                    native,
                    english,
                  },
                  startDate {
                    year,
                    month,
                    day,
                  },
                  endDate {
                    year,
                    month,
                    day,
                  },
                  status,
                  season,
                  format,
                  genres,
                  synonyms,
                  duration,
                  popularity,
                  episodes,
                  source(version: 2),
                  countryOfOrigin,
                  hashtag,
                  averageScore,
                  siteUrl,
                  description,
                  bannerImage,
                  isAdult,
                  coverImage {
                    extraLarge,
                    color,
                  },
                  trailer {
                    id,
                    thumbnail,
                  }
                  externalLinks {
                    site,
                    url,
                  },
                  rankings {
                    rank,
                    type,
                    season,
                    allTime,
                  },
                  studios(isMain: true) {
                    nodes {
                      id,
                      name,
                      siteUrl,
                    },
                  },
                  relations {
                    edges {
                      relationType(version: 2),
                      node {
                        id,
                        title {
                          romaji,
                          native,
                          english,
                        },
                        siteUrl,
                      },
                    },
                  },
                  airingSchedule(
                    notYetAired: true,
                    perPage: 2,
                  ) {
                    nodes {
                      episode,
                      airingAt,
                    },
                  },
                }
              }
            }
        ''')
        
        json_str = json.loads(res)
        res_data = json_str['data']
        next_page = res_data['Page']['pageInfo']['hasNextPage']
        page_data = res_data['Page']['media']
        last_page = res_data['Page']['pageInfo']['lastPage']

        print(f"Page: {page_num}, Remaining: {last_page-page_num}")

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
