# -*- coding:utf-8 -*-
from cmath import e
import enum
from http.client import PRECONDITION_REQUIRED
from locale import locale_encoding_alias
from jinja2 import Environment, FileSystemLoader
import sen_to_vec as vec
import wmd
import glob
import pandas as pd
import preproc as pre
import plot_dtw as dtw
import re
import numpy as np
import csv
import time

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
#tmpl = env.get_template('./html/tmp/temp01.html')
tmpl = env.get_template('./html/tmp/temp01_news_to_easy.html')

TS_DTW = 0.26
TS_WMD = 0.63

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


  # easy/newsをsource/targetへ変更
  source_sentence_num = n_sentence_num
  target_sentence_num = e_sentence_num
  source_word_list = n_word_list
  target_word_list = e_word_list
  source_vec_list = n_vec_list
  target_vec_list = e_vec_list
  directory_name = "news_to_easy/"

  #pair(number, source_sentence_num, target_sentence_num, source_word_list, target_word_list, source_vec_list, target_vec_list, directory_name)
  make_pseudo(source_sentence_num, source_word_list, target_word_list, source_vec_list, target_vec_list)


def make_pseudo(source_sentence_num, source_word_list, target_word_list, source_vec_list, target_vec_list):
  # DTWで単語間の距離を測る
  dist, path = dtw.path_vec(source_vec_list, target_vec_list)
  source_l, target_l = path_to_list(path)

  target_vec = []
  m = [source_sentence_num[i][0] for i , li in enumerate(source_sentence_num)]
  cnt_sentence = max(m)+1
  # 文のまとまりを抽出し、単語列のリストを作る。
  for k in range(0, cnt_sentence):
    n = [i for i, li in enumerate(source_sentence_num) if li[0] == k]
    
    if not n:
      break
    else:
      __s_start = min(n)
      __s_end = max(n)+1
      __t_start = target_l[source_l.index(min(n))]
      __t_end = target_l[last_index(source_l, max(n))]

      # 文単位でDTW
      if target_vec_list[__t_start:__t_end]:
        sentence_dist, sentence_path = dtw.path_vec(source_vec_list[__s_start:__s_end], target_vec_list[__t_start:__t_end])
        word_sum = len(source_vec_list[__s_start:__s_end]) * len(target_vec_list[__t_start:__t_end])
        wmd_dist = wmd.wmd_distance(source_word_list[__s_start:__s_end], target_word_list[__t_start:__t_end])
        data_line = [sentence_dist/word_sum, wmd_dist, "".join(source_word_list[__s_start:__s_end]), "".join(target_word_list[__t_start:__t_end])]
        with open('out/sentence_dist_dataset.csv',mode='a',encoding="utf-8") as cf:
          writer = csv.writer(cf, delimiter=",")
          writer.writerow(data_line)

      continue


# 表示
def pair(number, source_sentence_num, target_sentence_num, source_word_list, target_word_list, source_vec_list, target_vec_list, pname):
  # DTWで単語間の距離を測る
  dist, path = dtw.path_vec(source_vec_list, target_vec_list)
  source_l, target_l = path_to_list(path)

  source_list = []
  source_vec = []
  target_list = []
  target_vec = []
  distance_list = []
  wmd_list = []

  # 文のまとまりを抽出し、単語列のリストを作る。
  for k in range(0, len(source_sentence_num)):
    n = [i for i, li in enumerate(source_sentence_num) if li[0] == k]
    if not n:
#      print("105:if not n")
      break
    else:
      __s_start = min(n)
      __s_end = max(n)+1
      __t_start = target_l[source_l.index(min(n))]
      __t_end = target_l[last_index(source_l, max(n))]
      #print("number:", number, "__t_end:", __t_end, "len(target_l[]:", target_l[last_index(source_l, max(n))])

      source_list.append(" ".join(source_word_list[__s_start:__s_end]))
      target_list.append(" ".join(target_word_list[__t_start:__t_end]))

      source_vec.append(source_vec_list[__s_start:__s_end])
      target_vec.append(target_vec_list[__t_start:__t_end])

      # 文単位でDTW
      if not target_vec[k]:
#        print("target_vec is empty. k=", k, "len(target_vec)=", len(target_vec))
        distance_list.append(0)
        wmd_list.append(0)
      else:
        sentence_dist, sentence_path = dtw.path_vec(source_vec[k], target_vec[k])
        word_sum = len(source_vec[k]) * len(target_vec[k])
        sentence_dist_norm = round(sentence_dist/word_sum, 4)
        distance_list.append(sentence_dist_norm)
        wmd_list.append(wmd.wmd_distance(source_word_list[__s_start:__s_end], target_word_list[__t_start:__t_end]))

      continue

  with open('html/out/dtw_wmd.csv',mode='a',encoding="utf-8") as cf:
    writer = csv.writer(cf, delimiter=",")
    csv_data = list(zip(distance_list, wmd_list))
    writer.writerows(csv_data)

"""
  html = tmpl.render({"num_article":number, "data":zip(source_list, target_list, distance_list, wmd_list), "dtw_dist":dist})

  with open('html/out/' + pname + number +'.html',mode='w',encoding="utf-8") as f:
    f.write(str(html))
"""



if __name__=="__main__":
  start = time.perf_counter()

  for file in get_e_files():
    number = re.search('[0-9]+', file).group()
    view(number)

  print("TIME(s):", time.perf_counter() - start)
