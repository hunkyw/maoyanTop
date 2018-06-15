import json
import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool
#浏览器请求
def get_one_page(url):
    try:
        heads = {}
        heads['User-Agent'] = 'Mozilla/5.0 ' \
                              '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                              '(KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'

        response = requests.get(url,headers=heads)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
# 正则匹配
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            "score": item[5] + item[6]
        }
# 写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
# 主函数
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    # 多进程
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])