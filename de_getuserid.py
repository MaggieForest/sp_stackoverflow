# 获取原始问答的user_id

import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["stackoverflow_qa"]
my_col = my_db["qa_2017"]

for x in my_col.find():
    q_owner = x["q_owner"]
    answers = x["answers"]
    if "user_id" in q_owner:
        print(q_owner["user_id"])
        # 保存user_id为文档
        with open('D:/stackoverflow_json/2017_qa_user_id.txt', mode='a+', encoding='utf-8') as f:
            # write()将字符串写入到文件中
            f.write(str(q_owner["user_id"]) + "\n")
            f.close()
    if x["answers"] != None:
        for index in range(len(x["answers"])):
            if answers[index]["owner"]["user_type"] != "does_not_exist" :
                answer_user_id = answers[index]["owner"]["user_id"]
                print(str(answer_user_id))
                # 保存user_id为文档
                with open('D:/stackoverflow_json/2017_qa_user_id.txt', mode='a+', encoding='utf-8') as f:
                    # write()将字符串写入到文件中
                    f.write(str(answer_user_id)+ "\n")
                    f.close()
            else:
                print("回答用户已注销")
    else:
        print("答案为空")



