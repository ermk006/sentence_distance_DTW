from gensim.models import word2vec

model = word2vec.Word2Vec.load('./model/word2vec.model')
# print(model.wv["東京"])

similar_words = model.wv.most_similar(positive=["コロナ"], topn=9)
print(*[" ".join([v, str("{:.2f}".format(s))]) for v, s in similar_words], sep="\n")