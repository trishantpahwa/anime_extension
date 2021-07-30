import requests
from bs4 import BeautifulSoup
import timeit
import json


# url = 'https://kissanime.rest/anime/kuroko-no-basuke-2/12555/'
#url = 'https://kissanime.rest/anime/naruto-dub-/13765/'
url = input('Enter kissanum.rest url: ')

start_time = timeit.default_timer()

episode_count = 1

episodes = requests.get(url)
soup = BeautifulSoup(episodes.text, 'html.parser')
episodes_list = soup.find("ul", {"id": "episode_related"})
episodes_list = str(episodes_list).split('<li>')
_episodes = {}
for episode in episodes_list:
    if 'href=' in episode:
        try:
            print('Getting episode: ' + str(episode_count))
            
            __link = 'https://kissanime.rest' + episode.split('href=')[1].split('">\n')[0].split('" ')[1]
            num = episode.split('<div class="name"><span>EP</span>')[1].split('</div>')[0]
            episode = requests.get(__link)
            soup = BeautifulSoup(episode.text, 'html.parser')
            _link = soup.find("iframe")['src']
            temp_link = requests.get(_link)
            temp_link_soup = BeautifulSoup(temp_link.text, 'html.parser')
            __temp_link = temp_link_soup.find_all('li', {'class': 'linkserver'})
            for t in __temp_link:
                if 'gogo-play.net' in t['data-video']:
                    l = requests.get("https:" + t['data-video'])
                    _episodes[num] = l.text.split("sources:[{file: '")[1].split("',")[0]
            episode_count += 1
        except Exception as e:
            print(e)
            episode_count += 1

print(str(timeit.default_timer() - start_time) + ' to find links of ' + str(episode_count) + ' episodes.')

f = open(url.split('https://kissanime.rest/anime/')[1].split('/')[0] + '.json', 'w')
f.write(json.dumps(_episodes))
f.close()