# -*- coding:utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import sen_to_vec as vec
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))

tmpl = env.get_template('./html/tmp/temp01.html')

def view(f_easy, f_news, word_list=False, tokenizer="mecab"):
  with open(f_easy) as fe:
    lines_easy = fe.readlines()
    html = tmpl.render({"easy_sentences":lines_easy})

#  for i, line in enumerate(lines_easy):
#    vec_e, word_e = vec.to_vector(line, tokenizer)
#    print(word_e)
#    print("input1_len:",len(vec_e))


  with open(f_news) as fn:
    lines_news = fn.readlines()
    html = tmpl.render({"news_sentences":lines_news})

#  for j, line in enumerate(lines_news):
#    pass
  html = tmpl.render({"num_article":"001", "easy_sentences":lines_easy, "news_sentences":lines_news})


  with open('html/out/test.html',mode='w',encoding="utf-8") as f:
    f.write(str(html))

if __name__=="__main__":
  view("./data/easy/001.txt", "./data/news/001.txt")


"""
  vec_x, word_x = vec.to_vector(x, tokenizer)
  vec_y, word_y = vec.to_vector(y, tokenizer)

  print("input1_len:",len(vec_x))
  print("input2_len:",len(vec_y))

  if(word_list==True):
    print("easy:",word_x)
    print("news:",word_y)

  distance, path = fastdtw(vec_x, vec_y, dist=euclidean)
  print("distance:" ,distance)

  #print(path)
  #y1 = [1 for i in range(len(vec_x))]
  #y2 = [0 for i in range(len(vec_y))]

  print(path)
  for xi, yi in path:
    print(word_x[xi], ":", word_y[yi])
  


#商品情報を入れるリストを初期化
items=[]

#商品情報を入れる
items.append({"name":u'スマホ', "price":50000})
items.append({"name":u'充電器', "price":2000})
items.append({"name":u'フィルム', "price":500})

#書き出す
html = tmpl.render({"shop":u"アマズン", "items":items})

#htmlファイルとして書き出す
with open('jinja2_test.html',mode='w',encoding="utf-8") as f:
    f.write(str(html))


"""