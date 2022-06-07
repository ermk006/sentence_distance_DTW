from gensim.models import word2vec

model = word2vec.Word2Vec(corpus_file='./data/out_tokenizer.txt', window=5, min_count=1)
model.save("./model/word2vec.model")
