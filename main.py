from urllib import request, error
from bs4 import BeautifulSoup
import datetime
import json


class LirikLagu:
    """Crawling artist and song lyrics from https://lirik.kapanlagi.com"""
    data = {}

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

    def push_artist_song(self, artist_name, url_artist):
        pages = self.get_pagination_link(url_artist, {'class': 'col-lirik pagination'})
        if pages:
            print(pages)
        else:
            soup = self.soup_in_bowl(url_artist)
            songs = soup.find('ul', {'id': 'lyric-centerlist'}).find_all('a')
            for song in songs:
                song_url = song.get('href')
                song_title = song.text
                text_song = ""
                detail_songs = self.get_detail_song(song_url)
                for detail_song in detail_songs:
                    if detail_song.string != None :
                        text_song += "\n"
                        text_song += detail_song.text
                    else:
                        text_song += "\n"
                print(artist_name)
                print(song_url)
                print(song_title)
                print(text_song)

    def scrappy(self):
        pages = self.get_pagination_link(self.alphabet_link(), {'class': 'col-lirik pagination2'})
        for page in pages:
            soup = self.soup_in_bowl(page)
            artists = soup.find_all('div', {'class': 'div-horizontal2-list'})
            for artist in artists:
                artist_name = artist.a.text
                artist_url = artist.a.get('href')
                self.data[artist_name] = {'url': artist_url}
                self.push_artist_song(artist_name, artist_url)


def main():
    lirikLagu = LirikLagu()
    lirikLagu.scrappy()

if __name__ == '__main__':
    main()
