# 文章を形態素解析してベクトル列に変換する
import pandas as pd
import csv
import preproc as pre

comp_vector_list = "./out/pca3.csv"
sentence = "今日は暑い日だった。"

# 単語リストをベクトルリストへ変換
df = pd.read_csv(comp_vector_list, index_col=0, header=None)

def to_vector(sentence, tokenizer="mecab"):
  line = pre.pre(sentence)
  # 文を形態素解析＋原形に戻して単語リストへ
#  line = moji.zen_to_han(sentence, kana=False)
#  line = re.sub("[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3001-\u303F]", '', line)

  if(tokenizer=="ginza"):
    word_list = pre.ginza_tokenizer(line)
  else:
    word_list = pre.mecab_tokenizer(line)
  sentence_vec = []
  sentence_word = []
  for w in word_list:
    try:
      sentence_vec.append(list(df.loc[w]))
      sentence_word.append(w)
    except:
      print("NO WORD IN LIST!! :", w)
      pass

  return(sentence_vec, sentence_word)
