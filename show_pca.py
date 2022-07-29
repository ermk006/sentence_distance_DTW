# PCAの寄与率と固有値を求める
from operator import index
from gensim.models import KeyedVectors
from gensim.models import word2vec
import pandas as pd
import csv
import sklearn
from sklearn.decomposition import PCA

m_bi_file = './model/word2vec_mecab.model'
g_bi_file = './model/word2vec_ginza.model'

def show_pca(model_file):
  model = KeyedVectors.load_word2vec_format(model_file)

  df = pd.read_csv(model_file, encoding='UTF-8', sep=" ", header=None, index_col=None, skiprows=1)
  X = df.iloc[:, 1:]
  y = df.iloc[:, 0]

  pca = PCA()
  comp_X = pca.fit_transform(X)

  comp_data = pd.DataFrame(comp_X)

  print("寄与率")
  print(pd.DataFrame(pca.explained_variance_ratio_, index=["PC{}".format(x + 1) for x in range(len(X.columns))]).head(30))

  print("PCAの固有値")
  print(pd.DataFrame(pca.explained_variance_, index=["PC{}".format(x + 1) for x in range(len(X.columns))]).head(30))

  import numpy as np
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  plt.figure(figsize=(6, 4))
  plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
  plt.plot([0] + list( np.cumsum(pca.explained_variance_ratio_)), "-o")
  plt.xlabel("Number of principal components")
  plt.ylabel("Cumulative contribution rate")
  plt.grid()
  plt.savefig("out/pca_ratio.png")


if __name__=="__main__":
  print("which model? [1] mecab / [2] ginza")
  tokenizer = input("Press key [1] or [2]......")

  if(tokenizer == "1"):
    show_pca(m_bi_file)
  else:
    show_pca(g_bi_file)
  