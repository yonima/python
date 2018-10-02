'''

    明确任务：爬取豆瓣电影排行榜
    https://movie.douban.com/top250
'''

import requests
import re
import json


def get_one_page(url):
    '''
        抓取第一页内容
    :return: 请求的页面的信息
    '''

    try:
        #定义代理信息，为了防止爬虫
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }

        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            return response.text

        return None
    except RequestException:
        return None


def parse_one_page(html):
    '''
         使用正则表达式解析页面信息

    :param html:
    :return:
    '''
    
    #定义正则表达式样式
    '''
    '<ol>.*?pic.*?em.*?>(.*?)</em></ol>
        1. 获取页面信息：<title>(.*?)</title>
        2. 爬取电影片名信息：<li>.*?<em.*?\"\">(.*?)</em>
        3. 爬取电影图片链接信息：.*?href="(.*?)"
        4. 获取影片片名信息：.*?title.*?>(.*?)</span>.
        5. 获取影片主演，上映日期等信息:.*?\"\"(.*?)</p>'
        6. 获取电影评分 .*?rating_num.*?>(.*?)</span>
        7. 获取一句话简介 .*?inq.*?>(.*?)</span>
    '''
    #获取页面的信息：\n豆瓣电影 Top 250\n

    #pattern = re.compile('<title>(.*?)</title>', re.S)
    #爬取页面中的元素

    #获取电影的排名

    #pattern = re.compile('<em.*?\"\">(.*?)</em>', re.S)

    #获取电影的图片链接：.*?href="(.*?)"

    pattern = re.compile('<li>.*?<em.*?\"\">(.*?)</em>.*?href="(.*?)".*?title.*?>(.*?)</span>.*?\"\"(.*?)</p>.*?rating_num.*?>(.*?)</span>.*?inq.*?>(.*?)</span>', re.S)

    #findall方法获取所有匹配的信息，返回一个列表，里面的元素都是元组
    items = re.findall(pattern,html)

    print(items)
    #yield函数，生成字典格式更加好看
    for itme in items:
        yield{
            'range': itme[0],
            'image': itme[1],
            'title': itme[2],
            'infor': itme[3],
            'rating':itme[4],
            'intro':itme[5]
        }

def write_to_file(content):
    '''

          保存结果到CSV文件
    :param content:
    :return: 无
    '''

    with open('douban_movie_250.csv','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(start):
    '''

         定义主函数
    :return:
    '''

    #需要爬取的网页
    #url = 'https://movie.douban.com/top250'

    #爬取250个电影
    url = 'https://movie.douban.com/top250?start='+str(start)+'&filter='
    #https: // movie.douban.com / top250?start = 25 & filter =

    #爬取第一页
    html = get_one_page(url)
    #print(html)

    #解析爬取到的页面
    for item in parse_one_page(html):
        print (item)
        #保存结果
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(start= i* 25)
