from urllib import request, error
from bs4 import BeautifulSoup
import asyncio
import json


class LirikLagu:
    """Crawling artist and song lyrics from https://lirik.kapanlagi.com"""

    @staticmethod
    def alphabet_link():
        return 'https://lirik.kapanlagi.com/id/a/'

    @staticmethod
    def soup_in_bowl(link):
        url_req = ''
        req = request.Request(link)
        try:
            url_req = request.urlopen(req)
        except error.URLError as e:
            print(e.reason)
        soup = BeautifulSoup(url_req, 'html.parser')
        return soup

    def get_pagination_link(self, link, attr):
        links = []
        soup = self.soup_in_bowl(link)
        pages = soup.find('div', attr).find_all('a')
        for page in pages:
            if page.text:
                links.append(page.get('href'))
        return links

    def get_detail_song(self, link):
        soup = self.soup_in_bowl(link)
        song = soup.find('div', {'class': 'lyrics-body'}).find_all(["span", "br"])
        return song

    def get_song(self, url):
        artist_songs = {}
        soup = self.soup_in_bowl(url)
        songs = soup.find('ul', {'id': 'lyric-centerlist'}).find_all('a')
        for song in songs:
            song_url = song.get('href')
            song_title = song.text
            text_song = ""
            detail_songs = self.get_detail_song(song_url)
            for detail_song in detail_songs:
                if detail_song.string is not None:
                    text_song += "\n"
                    text_song += detail_song.text
                else:
                    text_song += "\n"
            if song_title:
                artist_songs[song_title] = {"title": song_title, "source": song_url, "lyrics": text_song}

        return artist_songs

    async def get_artist_song(self, url_artist):
        print(url_artist)
        artist_songs = {"songs": {}}
        pages = self.get_pagination_link(url_artist, {'class': 'col-lirik pagination'})
        if pages:
            for url_page in pages:
                artist_songs["songs"].update(self.get_song(url_page))
        else:
            artist_songs["songs"].update(self.get_song(url_artist))
        return artist_songs

    async def scrappy(self):
        pages = self.get_pagination_link(self.alphabet_link(), {'class': 'col-lirik pagination2'})
        data = {}
        for page in pages:
            soup = self.soup_in_bowl(page)
            artists = soup.find_all('div', {'class': 'div-horizontal2-list'})
            for artist in artists:
                artist_name = artist.a.text
                artist_url = artist.a.get('href')
                result = await self.get_artist_song(artist_url)
                data[artist_name] = {"results": result}
        return data


async def main():
    song_lyrics = LirikLagu()
    song_results = await song_lyrics.scrappy()
    with open('index.json', 'w') as file_json:
        json.dump(song_results, file_json)

if __name__ == '__main__':
    asyncio.run(main())
