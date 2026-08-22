import requests

class MetadataManager:
    @staticmethod
    def fetch_anime_info(anime_name: str) -> dict:
        """Busca sinopse e capa oficial do anime usando a API pública do AniList"""
        query = '''
        query ($search: String) {
          Media (search: $search, type: ANIME) {
            title {
              romaji
              english
              native
            }
            coverImage {
              large
            }
            description
            episodes
          }
        }
        '''
        variables = {'search': anime_name}
        url = 'https://graphql.anilist.co'

        try:
            response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
            if response.status_code == 200:
                data = response.json().get('data', {}).get('Media')
                if data:
                    titles = data.get('title', {})
                    official_title = titles.get('english') or titles.get('romaji') or anime_name
                    cover_img = data.get('coverImage', {}).get('large', '')
                    raw_desc = data.get('description', 'Sem descrição disponível.')
                    
                    return {
                        'title_official': official_title,
                        'cover': cover_img,
                        'description': raw_desc,
                        'total_episodes': data.get('episodes', 0)
                    }
        except Exception as e:
            print(f"Erro ao buscar metadados para {anime_name}: {e}")

        # Fallback caso a API falhe ou não encontre
        return {
            'title_official': anime_name,
            'cover': '',
            'description': 'Sem descrição disponível.',
            'total_episodes': 0
        }

