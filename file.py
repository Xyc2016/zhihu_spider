import requests
import re
from bs4 import BeautifulSoup


def get_content_str(url: str):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36'}
                        ).content.decode()


def get_top_answer_questions_urls(topic_id: str = '19561847', pages_n: int = 3):
    return set( ['http://www.zhihu.com' + url['href']
            for k in range(1, pages_n + 1)
            for url in BeautifulSoup(
            get_content_str('https://www.zhihu.com/topic/' + topic_id + '/top-answers?page=' + str(k))
            , 'html5lib').find_all(class_='question_link')])

top_answers_questions_urls = get_top_answer_questions_urls()

def get_photos(page_url: str):
    content_str = get_content_str(page_url)
    page_soup = BeautifulSoup(content_str, 'html5lib')
    photo_cards = page_soup.find_all(class_='origin_image zh-lightbox-thumb lazy')
    photo_urls = [card['data-original'] for card in photo_cards]
    import os
    if not os.path.exists(page_soup.title.string):
        os.mkdir(page_soup.title.string)
    cur_dir = page_soup.title.string
    k = 1
    for photo_url in photo_urls:
        k += 1
        with open(cur_dir + '/' + str(k) + '.jpg', 'wb') as photo_file:
            photo_file.write(requests.get(photo_url).content)


for page_url in top_answers_questions_urls:
    get_photos(page_url)
