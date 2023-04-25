import requests
class musicmatch:
    base_url = "https://api.musixmatch.com/ws/1.1/"
    parameters = '?format=json&callback=callback&'
    def __init__(self,api_key) -> None:
        self.api_key = f"&apikey={api_key}"

    def song_search(self,song_name, artist_name):
        method_url = 'matcher.lyrics.get'
        artist_name,song_name = artist_name.replace(' ', '%20'),song_name.replace(' ', '%20')
        song_json = requests.get(f'{self.base_url}{method_url}{self.parameters}q_artist={artist_name}&q_track={song_name}{self.api_key}').json()
        return song_json['message']['body']['lyrics']['lyrics_body']
        
mm = musicmatch('e859ba7bfe3d3583a83b95c619d248b7')
