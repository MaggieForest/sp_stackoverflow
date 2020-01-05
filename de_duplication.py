# userid去重

# 读取未去重的文件
with open('D:/stackoverflow_json/2017_qa_user_id.txt', mode='r', encoding='utf-8') as f:
    res = f.readlines()

    f.close()
print("未去重长度：" + str(len(res)))
# 转换为set数据
res = list(set(res))

# 去重
print("去重后长度：" + str(len(res)))

# 写入新文件
with open('D:/stackoverflow_json/de_duplication_2017_qa_user_id.txt', mode='a+', encoding='utf-8') as f:
    for i in res:
        f.write(i)
    f.close()