# display name 昵称
# reputation 用户 荣誉度
# age of account 账户的年龄(已经有了)
# badge count（金银铜） 金银铜分别的个数（有了）
# link 用户链接

import requests
from bs4 import BeautifulSoup


# 1.下载页面
def get_soup(url):
    res = ""
    try:
        ret = requests.get(url, timeout=15) # user_badges地址 eg. "https://stackoverflow.com/users/22656/jon-skeet?tab=badges&sort=recent&page=1"
    except Exception:
        ret = requests.get(url, timeout=20) # user_badges地址 eg. "https://stackoverflow.com/users/22656/jon-skeet?tab=badges&sort=recent&page=1"
    # html = ret.content.decode()  # 获取html字符串
    # html = etree.HTML(html)  # 获取element 类型的htm
    ret.encoding = ret.apparent_encoding  # 指定编码等于原始页面编码
    soup = BeautifulSoup(ret.text, 'lxml')  # 使用lxml则速度更快
    # print(str(soup))
    return soup


# 2.获取属性
def get_things(soup):
    # 昵称 display_name
    display_name = str(soup.select('#user-card > div > div.grid--cell.fl1.wmn0 > div > div.grid--cell.fl1 > div > div:nth-child(1) > h2 > div')[0].string)
    print("display_name:" + display_name)

    # 荣誉度
    reputation = int(str(soup.select('#avatar-card > div.my12.fw-normal.lh-sm > div > div.grid--cell.fs-title.fc-dark')[0].string).replace(",", ""))
    print("reputation:" + str(reputation))


    return display_name


user_id = "22656"
print("用户" + user_id + "相关信息：")
url = "https://stackoverflow.com/users/" + user_id + "?tab=profile"

print(url)
soup = get_soup(url)
get_things(soup)

























