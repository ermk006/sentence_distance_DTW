# -*- coding:utf-8 -*-
from locale import locale_encoding_alias
from jinja2 import Environment, FileSystemLoader
import sen_to_vec as vec
import glob
import pandas as pd

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
tmpl = env.get_template('./html/tmp/temp01.html')


# easyのファイルパス全てを取得
def get_e_files():
  files = glob.glob("./data/easy/*.txt")
  li_e_files = []
  for file in files:
    li_e_files.append(file)
  return li_e_files

# newsのファイルパス全てを取得
def get_n_files():
  files = glob.glob("./data/news/*.txt")
  li_n_files = []
  for file in files:
    li_n_files.append(file)
  return li_n_files

def view(f_easy, f_news, word_list=False, tokenizer="mecab"):
  with open(f_easy) as fe:
    lines_easy = fe.readlines()
    #print(lines_easy)

  e_sentence_num = []
  for i, line in enumerate(lines_easy):
    vec_e, word_e = vec.to_vector(line, tokenizer)
    for word in word_e:
      e_sentence_num.append([i, word])
  
  df_e = pd.DataFrame(e_sentence_num, columns=['e_num', 'e_word'])

  
  with open(f_news) as fn:
    lines_news = fn.readlines()

  n_sentence_num = []
  for i, line in enumerate(lines_news):
    vec_n, word_n = vec.to_vector(line, tokenizer)
    for word in word_n:
      n_sentence_num.append([i, word])

  df_n = pd.DataFrame(n_sentence_num, columns=['n_num', 'n_word']) 

#  print(pd.concat([df_e, df_n], axis=1))

'''
  html = tmpl.render({"num_article":"001", "easy_sentences":lines_easy, "news_sentences":lines_news})

  with open('html/out/test.html',mode='w',encoding="utf-8") as f:
    f.write(str(html))
'''

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