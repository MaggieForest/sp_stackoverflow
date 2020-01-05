# 获取用户历史提问的相关情况：
# post question count       用户历史中 发布的问题个数
# post question score       用户历史中 发布的问题获得的分数
# favorite question count   用户历史中 发布的问题 有多少被favorite过
# favorite question sum   用户历史中 发布的问题 有多少被favorite的总数 (计划爬取之外的数据)

import requests
from bs4 import BeautifulSoup
import re

# 1.下载页面
def get_soup(url):
    res = ""
    try:
        ret = requests.get(url, timeout=15) # user_badges地址 eg. "https://stackoverflow.com/users/22656/jon-skeet?tab=badges&sort=recent&page=1"
    except Exception:
        ret = requests.get(url, timeout=20)  # user_badges地址 eg. "https://stackoverflow.com/users/22656/jon-skeet?tab=badges&sort=recent&page=1"


    # html = ret.content.decode()  # 获取html字符串
    # html = etree.HTML(html)  # 获取element 类型的htm
    ret.encoding = ret.apparent_encoding  # 指定编码等于原始页面编码
    soup = BeautifulSoup(ret.text, 'lxml')  # 使用lxml则速度更快
    # print(str(soup))
    return soup


# 2.获得发布问题总数 question_count
def get_question_count(soup):
    question_count = soup.select("#user-tab-questions > div.subheader.user-full-tab-header > h1 > span")[0].string
    print("question_count:" + str(question_count))
    return question_count


# 3.获取本页被收藏个数 length，收藏总数favorite_question_sum
def get_favorite_question_count(soup):

    favorite_question_list = soup.select("#user-tab-questions > div.user-tab-content > div.user-questions > div.question-summary.narrow > div.favorites-count-off > b")
    favorite_question_sum = 0
    temp = 0
    length = len(favorite_question_list)
    for i in range(length):
        temp = favorite_question_list[i].string
        # print(temp)
        favorite_question_sum = int(favorite_question_sum) + int(temp)
    print("本页favorite_question_sum:" + str(favorite_question_sum))
    print("本页favorite_question_count:" + str(length))
    return favorite_question_sum, length


# 4.获取本页投票数 post_question_score
def get_post_question_score(soup):
    post_question_list = soup.select("#user-tab-questions > div.user-tab-content > div.user-questions > div.question-summary.narrow > div.question-counts.cp > div.votes > div.mini-counts")
    post_question_score = 0
    temp = 0
    length = len(post_question_list)
    for i in range(length):
        temp = post_question_list[i].string
        if str(temp).endswith("k"):
            temp = re.findall(r'\d+', str(post_question_list[i]))[0]
        # print(temp)
        # print("" + str(temp))
        post_question_score = int(post_question_score) + int(temp)
    print("本页post_question_score:" + str(post_question_score))
    return post_question_score


# 获取页数
def get_pages(question_count):
    pages = question_count//30
    left = question_count%30
    if left == 0 is True:
        pages = pages
    else:
        pages = pages+1
    print("pages=" + str(pages))
    print("====================================")
    return pages


def get(user_id):
    user_id = str(user_id)
    print("用户" + user_id + "提出的问题相关信息：")
    root_url = "https://stackoverflow.com/users/" + user_id + "/?tab=questions&sort=votes&page="

    url = str(root_url + str(1))
    print(url)

    soup = get_soup(url)
    # 此处获得提出问题数量 question_count
    question_count = int(get_question_count(soup).replace(",",""))
    # 获取页数
    pages = get_pages(question_count)
    favorite_question_count = 0
    favorite_question_sum = 0
    post_question_score = 0
    if pages == 1 is True:
        # 此处获得问题被favorite总数：favorite_question_count
        favorite_question_count = favorite_question_count + get_favorite_question_count(soup)
        post_question_score = post_question_score + get_post_question_score(soup)
        print("只有一页,已经执行：" + url)
        print("====================================")
    # else:
    else:
        # 更改链接+1，获得soup，get_favorite_question_count()
        for i in range(pages):
            url = str(root_url + str(i + 1))
            soup = get_soup(url)
            # 收藏总数favorite_question_sum, 收藏个数 favorite_question_count，
            curr_favorite_question_sum, curr_favorite_question_count = get_favorite_question_count(soup)
            favorite_question_sum = favorite_question_sum + curr_favorite_question_sum  # 收藏总数
            favorite_question_count = favorite_question_count + curr_favorite_question_count  # 被收藏过的问题总个数
            post_question_score = post_question_score + get_post_question_score(soup)

            print("当前favorite_question_count：" + str(favorite_question_count))
            print("当前favorite_question_sum：" + str(favorite_question_sum))
            print("当前post_question_score：" + str(post_question_score))
            print("已执行：" + url)
            print("====================================")

    print("***" + user_id + "***question_count*** = " + str(question_count))
    print("***" + user_id + "***favorite_question_count*** = " + str(favorite_question_count))
    print("***" + user_id + "***favorite_question_sum（计划之外）*** = " + str(favorite_question_sum))
    print("***" + user_id + "***post_question_score*** = " + str(post_question_score))
    return question_count, favorite_question_count, post_question_score

if __name__ == '__main__':
    get(22656)
