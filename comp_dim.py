# 学習済みword2vecモデルが100次元ベクトルなので、3次元に次元削減する。
import pandas as pd
from sklearn.decomposition import PCA
import time

start = time.perf_counter()

def comp(in_file, out_file):
  df = pd.read_csv(in_file, encoding='UTF-8', sep=" ", header=None, index_col=None, skiprows=1)
  X = df.iloc[:, 1:]
  y = df.iloc[:, 0]

  pca = PCA(n_components=3)
  comp_X = pca.fit_transform(X)

  comp_data = pd.DataFrame(comp_X)

  pca_df = pd.concat([y, comp_data], axis=1)
  pca_df.to_csv(out_file, index=False, header=None)

if __name__=="__main__":
  print("which model? [1] mecab / [2] ginza")
  tokenizer = input("Press key [1] or [2]......")

  if(tokenizer == "1"):
    print("compress vector of mecab model")
    comp("./model/word2vec_mecab.model", "./out/pca3_mecab.csv")
  elif(tokenizer == "2"):
    print("compress vector of ginza model")
    comp("./model/word2vec_ginza.model", "./out/pca3_ginza.csv")
  else:
    print("Press 1 or 2")
  
  print("TIME(s):", time.perf_counter() - start)

