# PCAの寄与率と固有値を求める
from operator import index
from gensim.models import KeyedVectors
from gensim.models import word2vec
import pandas as pd
import csv
import sklearn
from sklearn.decomposition import PCA

bi_file = './model/word2vec.model'
pca3_file = './out/pca3.csv'

model = KeyedVectors.load_word2vec_format(bi_file)

df = pd.read_csv(bi_file, encoding='UTF-8', sep=" ", header=None, index_col=None, skiprows=1)
X = df.iloc[:, 1:]
y = df.iloc[:, 0]

pca = PCA()
comp_X = pca.fit_transform(X)

comp_data = pd.DataFrame(comp_X)

print("寄与率")
print(pd.DataFrame(pca.explained_variance_ratio_, index=["PC{}".format(x + 1) for x in range(len(X.columns))]).head(10))

print("PCAの固有値")
print(pd.DataFrame(pca.explained_variance_, index=["PC{}".format(x + 1) for x in range(len(X.columns))]).head(10))

