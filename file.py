import requests
from bs4 import BeautifulSoup


def get_content_str(url: str):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36'}
                        ).content.decode()


def get_top_answer_questions_urls(topic_id: str = '19591186', pages_n: int = 3):
    return set(['http://www.zhihu.com' + url['href']
                for k in range(1, pages_n + 1)
                for url in BeautifulSoup(
            get_content_str('https://www.zhihu.com/topic/' + topic_id + '/top-answers?page=' + str(k))
            , 'html5lib').find_all(class_='question_link')])


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

def get_search_result(url:str):
    page = get_content_str(url)
    soup = BeautifulSoup(page,'html5lib')
    question_urls = [ 'http://www.zhihu.com' +card['href'] for card in soup.find_all(class_='js-title-link') if len(card['href'])==18]
    js_request = 'https://www.zhihu.com/r/search?q='+url[44:]+'&correction=1&type=content&offset=10'
    import json
    js_response_urls = [ BeautifulSoup(li,'html5lib').find_all(class_='js-title-link')[0]['href']  for li in  json.loads(get_content_str(js_request))['htmls'] ]
    while len(js_response_urls):
        for response_url in js_response_urls:
                if len(response_url)==18:
                    question_urls.append( 'http://www.zhihu.com'+ response_url)
        js_response_urls = [BeautifulSoup(card,'html5lib').find_all(class_='js-title-link')[0]['href'] for card in
                            json.loads(get_content_str(js_request))['htmls']]
    from pandas import DataFrame
    questions_tbl = DataFrame({'url':question_urls})
    questions_tbl.to_csv('result_of_search_'+url[44:]+'.csv')
    return question_urls

search_result = get_search_result(
    'https://www.zhihu.com/search?type=content&q=%E7%85%A7%E7%89%87'
)

for url in search_result:
    get_photos(url)

