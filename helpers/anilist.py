import requests
import discord

# Query para os dados sobre animes.
ANIME_QUERY = '''
query ($search: String) {
  Media(search: $search, type: ANIME) {
    id
    title {
      romaji
      native
    }
    status
    meanScore
    episodes
    nextAiringEpisode {
      timeUntilAiring
      airingAt
      episode
    }
    season
    seasonYear
    isLicensed
    externalLinks {
      site
      url
    }
    bannerImage
    siteUrl
    coverImage {
      large
    }
  }
}
'''


def get_title(data):
    return f"{data['title']['romaji']} • {data['title']['native']}"


def get_url(data):
    return f"[Página no Anilist]({data['siteUrl']})"


# Função responsável por "traduzir" o status da media e
# retornar a cor desse status.
def get_status(data):
    status = data['status']
    if status == "RELEASING":
        return ['Em andamento', 0x4BE172]
    elif status == "FINISHED":
        return ['Finalizado', 0x414DC7]
    elif status == "NOT_YET_RELEASED":
        return ['Ainda não lançado', 0xEBE3EF]
    elif status == "CANCELLED":
        return ['Cancelado', 0xE35656]
    elif status == "HIATUS":
        return ['Hiato', 0xF3F36B]


# O Embed aqui pode ser generalizado tanto para animes quanto para mangás.
def create_base_embed(data):
    # Status do anime [Lançando, Finalizado, etc.]
    status = get_status(data)
    # Aqui é o corpo do embed
    embed = discord.Embed(
        title=get_title(data),
        description=get_url(data),
        colour=status[1]
    )
    # A imagem do banner da página do anime pode ser nula,
    # caso o anime não tenha publicado nada
    banner_image = data["bannerImage"]
    # Só será colocado caso o valor não seja 'None'
    if banner_image:
        embed.set_image(url=banner_image)
    # Inline faz os fields do Embed ficarem lado-a-lado,
    # porém há um limite de tamanho
    embed.add_field(name="Status", value=status[0], inline=True)
    return embed


def get_anime_data(name):
    # Variáveis para o request POST no Anilist
    variables = {'search': name}
    # URL para o request
    url = 'https://graphql.anilist.co'
    # Dict dos dados do Anime
    data = requests.post(
        url, json={'query': ANIME_QUERY, 'variables': variables}).json()
    return data['data']['Media']


def create_anime_embed(name):
    # JSON dos dados do anime
    data = get_anime_data(name)
    # Embed base para adicionar os dados específicos de anime
    embed = create_base_embed(data)
    return embed


def anime(name):
    embed = create_anime_embed(name)
    return embed
