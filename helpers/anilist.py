import requests
import asyncio


anime_query = '''
query ($search: String) {
  Media (search: $search, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
    id
    title {
      romaji
      english
      native
    }
  }
}'''


async def anime(anime_name):
    variables = {'search': anime_name}
    response = requests.post('https://graphql.anilist.co', json={'query': anime_query, 'variables': variables})
    print(response.json())
