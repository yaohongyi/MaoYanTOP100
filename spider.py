# -*- coding: UTF-8 -*-
import json
import re
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        # 请求猫眼电影榜单TOP100的首页
        response = requests.get(url)
        # 如果返回状态为200，则返回网页内容
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求出错！', url)
def get_film_info(html):
    # 定义正则表达式，分别提取网页中的电影图片地址、电影详情URL、电影名称、主演、上映时间、评分
    pattern = re.compile('<dd>.*?<img data-src="(http.*?)".*?'
                         '<p.*?<a href="(.*?)" title="(.*?)".*?</a></p>.*?'
                         '<p.*?>(.*?)</p>.*?'
                         '<p.*?>(.*?)</p>.*?'
                         '<p.*?><i.*?>(.*?)</i><i.*?>(\d)</i></p>', re.S)
    # 利用正则表达式提取内容，提取出来的是由元组组成的列表
    result = re.findall(pattern, html)
    # 创建迭代器，遍历正则表达式提取的内容，将其组装成字典
    for i in result:
        yield {
            'image_url': i[0],
            'film_detail_url': 'http://maoyan.com' + i[1],
            'film_name': i[2],
            'star': i[3].strip()[3:],
            'release_time': i[4].strip()[5:],
            'score': i[5] + str(i[6])}
def save_to_file(content):
    # open函数打开文件，a参数在文件中追加内容，内容编码方式设定为'utf-8'
    with open('MaoYanTOP100.txt', 'a', encoding='utf-8') as f:
        # json.dumps将Python字典转换成json，指定ensure_ascii使用ascii编码外的其他编码
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(offset):
    # TOP100榜单有10页，拼接请求地址
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    # 获取请求地址页面内容
    response = get_one_page(url)
    # 正则表达式提取页面影片信息，result是一个迭代器
    result = get_film_info(response)
    for i in result:
        # 打印单个影片信息
        print(i)
        # 将影片信息保存到文件中
        save_to_file(i)

if __name__ == '__main__':
    # 创建线程池
    pool = Pool()
    # 多线程执行main方法，offset是用来控制TOP100请求地址参数的，参数规律是0-10-20...
    pool.map(main, [offset*10 for offset in range(10)])