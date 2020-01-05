from bs4 import BeautifulSoup
import requests
import re

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
    soup = BeautifulSoup(ret.text, 'lxml')  # 使用lxml则速度更快 html.parser
    # print(str(soup))
    return soup


# 获取该用户有多少种badge,返回应爬取的页数
def get_badgeCount(soup, user_id):
    str_class_count = soup.select("#user-tab-badges > div.subheader.user-full-tab-header > h1 > span")
    if len(str_class_count) != 0: #如果不是page not found
        # print(str(soup))
        # print(str_class_count)
        count = str(str_class_count[0])
        p1 = re.compile(r'[>](.*?)[<]', re.S)
        class_count = re.findall(p1, count)[0]
        print("获得badge种类数：" + class_count)
        class_count = atoi(class_count)# base为进制基数
        pages = class_count//52
        left = class_count%52
        if left == 0 is True:
            pages = pages
        else:
            pages = pages+1
        print("pages=" + str(pages))
        return class_count, pages
    else:
        # id记录到pagenotfound文件
        print("id记录到pagenotfound文件")
        with open("D:/stackoverflow_json/page_not_found.txt", 'a') as page_not_found_file:
            page_not_found_file.write(user_id + "\n")
            # print("xieruwancheng ")
            page_not_found_file.close()
        return "exception", "exception"



# 2.得到badges:
# 包含： badge_url;  badge_name;  num    三个属性
# (注意badges 包含.的时候，在链接里记得删除   如： .net-core --> url:"/help/badges/6057/net-core?userid=" )
def get_Badges(soup):
    td_list = soup.select('#user-tab-badges > div.user-tab-content > table > tbody > tr > td')
    curr_paqe_badge = [] #储存本页所有badge
    for badge in td_list:
        badge_info = []
        badge = str(badge).replace("\n","")
        #str_1：badge的url
        str_1 = str(str(badge).split('"')[3]).split("?")[0] # 用"截取到badge链接，再截取？前面的字符
        # print("str_1：" + str_1)
        badge_info.append(str_1)

        #str_2：badge_name
        str_2 = str(str(badge).split("></span>")[1]).split("</a>")[0].lstrip()
        # print("str_2：" + str_2)
        badge_info.append(str_2)

        #str_3：num
        if badge.endswith("</span></span></td>"):
            str_3 = str(badge).split("</span> <span ")[1].lstrip("class=\"item-multiplier-count\">").rstrip("</span></span></td>")
            # print("str_3：" + str_3)
            badge_info.append(str_3)
        else:
            # print("str_3：1")
            badge_info.append("1")

        #打印检验
        # print(str(badge_info))
        curr_paqe_badge.append(badge_info) #本页所有badge信息，包括 链接，名字，获得数量
    return curr_paqe_badge


def atoi(num_string):
    if num_string == '':
        return 0
    else:
        try:
            f = float(num_string)
            i = int(f)
        except:
            return 0
        else:
            return i

def get(user_id):
    user_id = str(user_id)
    root_url = "https://stackoverflow.com/users/" + user_id + "/?tab=badges&sort=recent&page="
    # print(root_url)
    url = str(root_url + str(1))
    soup = get_soup(url)
    class_count, pages = get_badgeCount(soup, str(user_id))
    print(class_count, pages)
    paqe_badge = []
    if str(class_count) == "exception":
        print("exception true")
        return "exception"
    elif pages == 1 is True:
        paqe_badge = get_Badges(soup)
        print("只有一页,已经执行：" + url)
        return paqe_badge
    else:
        # 更改链接+1，获得soup，get_Badges()
        for i in range(pages):
            url = str(root_url + str(i+1))
            soup = get_soup(url)
            paqe_badge.extend(get_Badges(soup))
            print("已执行：" + url)
        return paqe_badge

if __name__ == '__main__':
    get(22656)

