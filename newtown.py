from urllib.parse import unquote
import urllib.request
import os
import html

import requests
import re


def process_line(line):
    tags = [line.get('Tag 1'),
            line.get('Tag 2'),
            line.get('Tag 3'),
            line.get('Tag 4'),
            line.get('Tag 5')]
    tags = [t.lower() for t in tags if t is not None]
    episodes = [
        line.get('episode 1'),
        line.get('episode 2'),
        line.get('episode 3'),
        line.get('episode 4'),
        line.get('episode 5'),
    ]
    episodes = [e for e in episodes if e is not None]
    return tags, episodes
mp3_url_regex = re.compile(r'href="(?P<url>http:\/\/newtownradio.com\/newtown\/audio\/(?P<folder>[^\/]+)\/(?P<file>[^\/]+.mp3))" title="(?P<title>.+)"')
mp3_url_reverse_regex = re.compile(r'title="(?P<title>.+)" href="(?P<url>http:\/\/newtownradio.com\/newtown\/audio\/(?P<folder>[^\/]+)\/(?P<file>[^\/]+.mp3))"')

def get_mp3_url_from_show_archive(url):
    response = requests.get(url)
    raw_html = response.content.decode('utf-8')

    matches = mp3_url_regex.search(raw_html)
    reverse_matches = mp3_url_reverse_regex.search(raw_html)

    matches = matches or reverse_matches

    if not matches:
        raise ValueError(f'Could not find mp3 url in {url}')

    matches = matches.groupdict()
    folder = unquote(matches['folder'])
    file = unquote(matches['file'])
    file_url = matches['url']
    title = html.unescape(matches['title'])
    file_loc = f'./{folder}/{file}'
    if not os.path.exists(folder):
        os.mkdir(folder)
    urllib.request.urlretrieve(file_url, file_loc)

    return file_loc, title