# 1.获取
# post answer count 用户历史中       发布的答案 个数
# post answer score 用户历史中       发布的答案获得的分数
# accept answer count 用户历史       发布的回答有多少被accepted

# post question count       用户历史中 发布的问题个数
# post question score       用户历史中 发布的问题获得的分数
# favorite question count   用户历史中 发布的问题 有多少被favorite过

# 2.保存到json文件中

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import sp_Stackoverflow.fetch_user_badges as badges
import sp_Stackoverflow.fetch_post_answer_things as answers
import sp_Stackoverflow.fetch_post_question_things as questions
import json


def run(user_id):
    page_badge = badges.get(user_id)
    # 如果有错误
    if page_badge == "exception":
        return "exception", "exception", "exception", "exception", "exception", "exception", "exception"
    answer_count, accept_answer_count, post_answer_score = answers.get(user_id)
    question_count, favorite_question_count, post_question_score = questions.get(user_id)
    return page_badge, answer_count, accept_answer_count, post_answer_score, question_count, favorite_question_count, post_question_score


if __name__ == '__main__':

    # 读取去重的user_id list
    user_id_file = open("D:/stackoverflow_json/de_duplication_2017_qa_user_id.txt")

    while 1:
        line = user_id_file.readline()
        if not line:
            break
        curr_user_id = line.replace("\n","")
        print("curr_user_id:" + curr_user_id)

        # 运行爬取
        page_badge, answer_count, accept_answer_count, post_answer_score, question_count, favorite_question_count, post_question_score = run(curr_user_id)
        if page_badge == "exception":
            continue
        print("*********************************************************************************************")
        for i in page_badge:
            print(str(i))
        print("answer_count:" + str(answer_count))
        print("accept_answer_count:" + str(accept_answer_count))
        print("post_answer_score:" + str(post_answer_score))
        print("question_count:" + str(question_count))
        print("favorite_question_count:" + str(favorite_question_count))
        print("post_question_score:" + str(post_question_score))

        # 保存为json
        user_dict = {}
        user_dict["user_id"] = curr_user_id
        user_dict["page_badge"] = page_badge
        user_dict["answer_count"] = answer_count
        user_dict["accept_answer_count"] = accept_answer_count
        user_dict["post_answer_score"] = post_answer_score
        user_dict["question_count"] = question_count
        user_dict["favorite_question_count"] = favorite_question_count
        user_dict["post_question_score"] = post_question_score
        user_json_str = json.dumps(user_dict, ensure_ascii=False)  # 将字典装化为json串
        with open("D:/stackoverflow_json/user.json", 'a') as f_write:
            f_write.write(user_json_str + ',\n')
            f_write.close()

    user_id_file.close()