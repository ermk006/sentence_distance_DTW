# 文章を形態素解析してベクトル列に変換する
import pandas as pd
import preproc as pre

#vector_list_m = "./out/pca3_mecab.csv"
vector_list_m = "./out/pca30_mecab.csv"
vector_list_g = "./out/pca3_ginza.csv"

# 単語リストをベクトルリストへ変換
df_m = pd.read_csv(vector_list_m, index_col=0, header=None)
df_g = pd.read_csv(vector_list_g, index_col=0, header=None)

def to_vector(sentence, tokenizer="mecab"):
  line = pre.pre(sentence)

  if(tokenizer=="ginza"):
    word_list = pre.ginza_tokenizer(line)
    df = df_g
  else:
    word_list = pre.mecab_tokenizer(line)
    df = df_m
  
  sentence_vec = []
  sentence_word = []
  for w in word_list:
    try:
      sentence_vec.append(list(df.loc[w]))
      sentence_word.append(w)
    except:
      print("NO WORD IN LIST!! :", w)
      sentence_vec.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
#      sentence_vec.append([0, 0, 0])
      sentence_word.append(w)
      pass

  return(sentence_vec, sentence_word)
