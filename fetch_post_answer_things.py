# post answer count 用户历史中       发布的答案 个数
# post answer score 用户历史中       发布的答案获得的分数
# accept answer count 用户历史       发布的回答有多少被accepted

import requests
from bs4 import BeautifulSoup


# 1.下载页面
def get_soup(url):
    res = ""
    try:
        ret = requests.get(url, timeout=15) # user_badges地址 eg. "https://stackoverflow.com/users/22656/jon-skeet?tab=badges&sort=recent&page=1"
    except Exception:
        ret = requests.get(url,timeout=20)  # user_badges地址 eg. "https://stackoverflow.com/users/22656/jon-skeet?tab=badges&sort=recent&page=1"
    # html = ret.content.decode()  # 获取html字符串
    # html = etree.HTML(html)  # 获取element 类型的htm
    ret.encoding = ret.apparent_encoding  # 指定编码等于原始页面编码
    soup = BeautifulSoup(ret.text, 'lxml')  # 使用lxml则速度更快
    # print(str(soup))
    return soup


# 2.发布的答案个数 answer count
def get_answer_count(soup):
    answer_count = str(soup.select('#user-tab-answers > div.subheader.user-full-tab-header > h1 > span')[0].string).replace(",", "")
    print("answer_count:" + str(answer_count))
    return answer_count


# 3.获取本页被accept的回答个数 accept_answer_count ，本页分数post_answer_score
def get_accept_answer_count(soup):
    # print(type(soup))
    accept_list = soup.select('#user-tab-answers > div.user-tab-content > div.user-answers > div.answer-summary > div.answer-votes')
    post_answer_score = 0
    list_string = ""
    for i in range(len(accept_list)):
        post_answer_score = post_answer_score + int(str(accept_list[i].string).strip().replace("\\n", ""))
        list_string = list_string + str(accept_list[i]) # 拼接起来构造bs，继续select accepted
    # accept_answer_list = soup.select('#user-tab-answers > div.user-tab-content > div.user-answers > div.answer-summary > div.answered-accepted')
    accept_answer_list = BeautifulSoup(list_string, features="lxml").select('div.answered-accepted')
    length = len(accept_answer_list)
    print("本页accept_answer_count:" + str(length))
    print("本页post_answer_score:" + str(post_answer_score))
    return length,post_answer_score


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
    print("用户" + user_id + "做出的回答相关信息：")
    root_url = "https://stackoverflow.com/users/" + user_id + "?tab=answers&sort=votes&page="
    url = str(root_url + str(1))
    print(url)
    soup = get_soup(url)
    # 此处获得提出问题数量 question_count
    answer_count = int(get_answer_count(soup))
    # 获取页数
    pages = get_pages(answer_count)

    accept_answer_count = 0
    post_answer_score = 0

    if pages == 1 is True:
        # 此处获得问题被accept总数：accept_answer_count ,分数 post_answer_score
        accept_answer_count,post_answer_score = accept_answer_count + get_accept_answer_count(soup)
        # post_question_score = post_question_score + get_post_question_score(soup)
        print("只有一页,已经执行：" + url)
        print("====================================")
    else:
        # 更改链接+1，获得soup，get_accept_answer_count()
        for i in range(pages):
            url = str(root_url + str(i+1))
            soup = get_soup(url)
            # 此处获得问题被accept总数：accept_answer_count
            curr_accept_answer_count, curr_post_answer_score = get_accept_answer_count(soup)
            accept_answer_count = accept_answer_count + curr_accept_answer_count # 回答问题被accept个数
            post_answer_score = post_answer_score + int(curr_post_answer_score)

            # post_question_score = post_question_score + get_post_question_score(soup)

            print("当前accepted_answer_count：" + str(accept_answer_count))
            # print("当前post_question_score：" + str(post_question_score))
            print("已执行：" + url)
            print("====================================")

    print("***" + user_id + "***answer_count*** = " + str(answer_count))
    print("***" + user_id + "***accept_answer_count*** = " + str(accept_answer_count))
    print("***" + user_id + "***post_answer_score*** = " + str(post_answer_score))
    return answer_count, accept_answer_count, post_answer_score

if __name__ == '__main__':
    get(1783632)