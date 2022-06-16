from operator import index
from gensim.models import KeyedVectors
from gensim.models import word2vec
import pandas as pd
import csv
import sklearn
from sklearn.decomposition import PCA

bi_file = './model/word2vec.model'
pca3_file = './out/pca3.csv'

#model = word2vec.Word2Vec.load(bi_file)
model = KeyedVectors.load_word2vec_format(bi_file)
# print("[vocab count]",model.vectors.shape[0])


# 全部の単語リストとベクトルを取り出してcsvから読み込む
#for word in model.vocab:
#    print(word, model[word])

df = pd.read_csv(bi_file, encoding='UTF-8', sep=" ", header=None, index_col=None, skiprows=1)
X = df.iloc[:, 1:]
y = df.iloc[:, 0]

pca = PCA(n_components=3)
comp_X = pca.fit_transform(X)

comp_data = pd.DataFrame(comp_X)

'''
print(y.shape)
print(y.head(100))
print(comp_data.head(100))
print(comp_data.shape)
'''
pca_df = pd.concat([y, comp_data], axis=1)
pca_df.to_csv(pca3_file, index=False, header=None)

