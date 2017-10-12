# -*- coding: utf-8 -*-
import urllib2
from HTMLParser import HTMLParser

class MovieParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None

        if tag == 'li' and _attr(attrs, 'data-title') and _attr(attrs, 'data-category') == 'nowplaying':
            movie = {}
            movie['title'] = _attr(attrs, 'data-title')
            movie['score'] = _attr(attrs, 'data-score')
            movie['director'] = _attr(attrs, 'data-director')
            movie['actors'] = _attr(attrs, 'data-actors')
            self.movies.append(movie)
            print('%(title)s|%(score)s|%(director)s|%(actors)s' % movie)

    def saveinfo(self, movie ):
        f = open('info.txt','a')
        for each in movie3:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('score:' + each['score'] + '\n')
            f.writelines('director:' + each['director'] + '\n')
            f.writelines('actors:' + each['actors'] + '\n\n')
            #f.writelines('learnnum:' + each['learnnum'] +'\n\n')
        f.close()


def nowplaying_movies(url):
    #User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    req = urllib2.Request(url, headers=headers)
    s = urllib2.urlopen(req)
    parser = MovieParser()
    parser.feed(s.read())
    s.close()
    return parser.movies


if __name__ == '__main__':
    url = 'http://movie.douban.com/nowplaying/xiamen/'
    movies = nowplaying_movies(url)

    import json
    print('%s' % json.dumps(movies, sort_keys=True, indent=4, separators=(',', ': ')))
    for each in movies:
        info = movies.getinfo(each)
        movies.append(info)
    movies.saveinfo(movie=movies)