# コーパスからword2vecモデルを生成する
from gensim.models import word2vec
from gensim.models import KeyedVectors

model = word2vec.Word2Vec(corpus_file='./out/token.txt', vector_size=100, window=5, min_count=1)
model.wv.save_word2vec_format("./model/word2vec.model")
#model.save("./model/word2vec.model")