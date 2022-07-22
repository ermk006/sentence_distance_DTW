# -*- coding:utf-8 -*-
from cmath import e
import enum
from http.client import PRECONDITION_REQUIRED
from locale import locale_encoding_alias
from jinja2 import Environment, FileSystemLoader
import sen_to_vec as vec
import glob
import pandas as pd
import preproc as pre
import plot_dtw as dtw
import re

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


def path_to_list(path):
    return [list(r) for r in zip(*path)]


def last_index(li, x):
  num = [i for i, _x in enumerate(li) if _x == x]
  return num[-1]

def view(number, tokenizer="mecab"):
  f_easy = "./data/easy/" + number + ".txt"
  f_news = "./data/news/" + number + ".txt"

  with open(f_easy) as fe:
    lines_easy = fe.readlines()
    #print(lines_easy)

  e_sentence_num = []
  e_vec_list = []
  e_word_list = []
  for i, line in enumerate(lines_easy):
    vec_e, word_e = vec.to_vector(pre.pre(line), tokenizer)
    e_vec_list.extend(vec_e)
    e_word_list.extend(word_e)
    for word in word_e:
      e_sentence_num.append([i, word])
  
  with open(f_news) as fn:
    lines_news = fn.readlines()

  n_vec_list = []
  n_sentence_num = []
  n_word_list = []
  for i, line in enumerate(lines_news):
    vec_n, word_n = vec.to_vector(pre.pre(line), tokenizer)
    n_vec_list.extend(vec_n)
    n_word_list.extend(word_n)
    num_line = i
    for word in word_n:
      n_sentence_num.append([i, word])

  # DTWで単語間の距離を測る
  dist, path = dtw.path_vec(e_vec_list, n_vec_list)
  e_l, n_l = path_to_list(path)
  

  # 表示
  easy_list = []
  news_list = []
  for k in range(0, len(e_sentence_num)):
    n = [i for i, li in enumerate(e_sentence_num) if li[0] == k]
    if(len(n) > 1):
      easy_list.append(" ".join(e_word_list[min(n):max(n)+1]))
      news_list.append(" ".join(n_word_list[n_l[e_l.index(min(n))]:n_l[last_index(e_l, max(n))]]))

#  html = tmpl.render({"num_article":number, "data":zip(easy_list, news_list)})

#  with open('html/out/' + number +'.html',mode='w',encoding="utf-8") as f:
#    f.write(str(html))

if __name__=="__main__":
  for file in get_e_files():
    print(file)
    number = re.search('[0-9]+', file).group()
    view(number)
