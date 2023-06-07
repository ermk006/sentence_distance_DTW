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
import os

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
test_files = ["022.txt", "186.txt", "169.txt"]

output_path = "out_biDirectional/raw_sentence_dist_dataset_EtoN.csv"
split_mode = "full_sentence" #完成文にするなら"full_sentence"にする

if(os.path.isfile(output_path)):
    os.remove(output_path)

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

def search_range(li, x):
  min = li.index(x)
  max = last_index(li, x)
  return min, max

def view(number, directions, tokenizer="mecab"):
  f_easy = "./data/easy/" + number + ".txt"
  f_news = "./data/news/" + number + ".txt"

  # テキストから単語ベクトル、文番号、原形単語、生単語をリスト化
  with open(f_easy) as fe:
    lines_easy = fe.readlines()

  e_sentence_num = []
  e_vec_list = []
  e_word_list = []
  e_raw_list = []
  for i, line in enumerate(lines_easy):
    vec_e, word_e = vec.to_vector(pre.pre(line), tokenizer)
    e_raw_list.extend(pre.mecab_wakati_raw(pre.pre(line)))
    e_vec_list.extend(vec_e)
    e_word_list.extend(word_e)
    for word in word_e:
      e_sentence_num.append([i, word])
  
  with open(f_news) as fn:
    lines_news = fn.readlines()

  n_vec_list = []
  n_sentence_num = []
  n_word_list = []
  n_raw_list = []
  for i, line in enumerate(lines_news):
    vec_n, word_n = vec.to_vector(pre.pre(line), tokenizer)
    n_raw_list.extend(pre.mecab_wakati_raw(pre.pre(line)))  #全角数字は1文字ずつ分かち書きされてしまう
    n_vec_list.extend(vec_n)
    n_word_list.extend(word_n)
    for word in word_n:
      n_sentence_num.append([i, word])

  # easy->newsの対応づけか？news->easyの対応づけか？
  if(directions == "to_easy"):
    # easy/newsをsource/targetへ変更
    source_sentence_num = n_sentence_num
    target_sentence_num = e_sentence_num
    source_word_list = n_word_list
    target_word_list = e_word_list
    source_raw_list = n_raw_list
    target_raw_list = e_raw_list
    source_vec_list = n_vec_list
    target_vec_list = e_vec_list
  else: # to_news
    # news/easyをsource/targetへ変更
    source_sentence_num = e_sentence_num
    target_sentence_num = n_sentence_num
    source_word_list = e_word_list
    target_word_list = n_word_list
    source_raw_list = e_raw_list
    target_raw_list = n_raw_list
    source_vec_list = e_vec_list
    target_vec_list = n_vec_list


  # DTWで単語間の距離を測る
  dist, path = dtw.path_vec(source_vec_list, target_vec_list)
  source_l, target_l = path_to_list(path)

  source_sentence_list = [source_sentence_num[i][0] for i , li in enumerate(source_sentence_num)]
  target_sentence_list = [target_sentence_num[i][0] for i , li in enumerate(target_sentence_num)]
  s_cnt_sentence = max(source_sentence_list)+1

  # 文のまとまりを抽出し、単語列のリストを作る。
  for k in range(0, s_cnt_sentence):
    n = [i for i, li in enumerate(source_sentence_num) if li[0] == k]

    
    if not n:
      break
    else:
      __s_start = min(n)
      __s_end = max(n)+1

      if split_mode == "full_sentence":
        s_t_pos = target_l[source_l.index(min(n))]
        s_e_pos = target_l[last_index(source_l, max(n))]+1
        __t_start, _ = search_range(target_sentence_list, target_sentence_num[s_t_pos][0])
        _, __t_end = search_range(target_sentence_list, target_sentence_num[s_e_pos-1][0])
      else:
        __t_start = target_l[source_l.index(min(n))]
        __t_end = target_l[last_index(source_l, max(n))]

      # 文単位でDTW
      if target_vec_list[__t_start:__t_end+1]:
        sentence_dist, sentence_path = dtw.path_vec(source_vec_list[__s_start:__s_end], target_vec_list[__t_start:__t_end+1])
        word_sum = len(source_vec_list[__s_start:__s_end]) * len(target_vec_list[__t_start:__t_end+1])
        wmd_dist = wmd.wmd_distance(source_word_list[__s_start:__s_end], target_word_list[__t_start:__t_end+1])

        data_line = [sentence_dist/word_sum, wmd_dist, "".join(source_raw_list[__s_start:__s_end]), "".join(target_raw_list[__t_start:__t_end+1])]

        with open(output_path, mode='a',encoding="utf-8") as cf:
          writer = csv.writer(cf, delimiter=",")
          writer.writerow(data_line)

      continue


if __name__=="__main__":
  start = time.perf_counter()
  mode = get_e_files()
#  mode = test_files
  print(mode)

  for file in mode:
    number = re.search('[0-9]+', file).group()
    print("[fnum]",number)
    view(number, "to_news")

  print("TIME(s):", time.perf_counter() - start)
