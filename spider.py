# -*- coding: UTF-8 -*-
import json
import re
import requests
from multiprocessing import Pool


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None
def get_film_info(html):
    pattern = re.compile('<dd>.*?<img data-src="(http.*?)".*?'
                         '<p.*?<a href="(.*?)" title="(.*?)".*?</a></p>.*?'
                         '<p.*?>(.*?)</p>.*?'
                         '<p.*?>(.*?)</p>.*?'
                         '<p.*?><i.*?>(.*?)</i><i.*?>(\d)</i></p>', re.S)
    result = re.findall(pattern, html)
    for i in result:
        yield {
            'image_url': i[0],
            'film_detail_url': 'http://maoyan.com' + i[1],
            'film_name': i[2],
            'star': i[3].strip()[3:],
            'release_time': i[4].strip()[5:],
            'score': i[5] + str(i[6])}
def save_to_file(content):
    with open('MaoYanTOP100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    response = get_one_page(url)
    result = get_film_info(response)
    for i in result:
        print(i)
        save_to_file(i)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [offset*10 for offset in range(10)])