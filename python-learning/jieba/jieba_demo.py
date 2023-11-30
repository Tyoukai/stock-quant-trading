import jieba

test_content = '我对你的爱就像大海一样宽广'
cut_res = jieba.cut(test_content)
print(list(cut_res))

# 精准模式，适合文本分析
cut_res1 = jieba.cut(test_content, cut_all=False)
print('精准模式:', list(cut_res1))
