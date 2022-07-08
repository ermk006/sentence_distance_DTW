# コーパスからword2vecモデルを生成する
from gensim.models import word2vec
from gensim.models import KeyedVectors
import time

start = time.perf_counter()

def mk_model(corpus_file, modelfile):
  model = word2vec.Word2Vec(corpus_file=corpus_file, vector_size=100, window=5, min_count=1)
  model.wv.save_word2vec_format(modelfile)
  #model.save("./model/word2vec.model")

if __name__=="__main__":
  print("which model? [1] mecab / [2] ginza")
  tokenizer = input("Press key [1] or [2]......")

  if(tokenizer == "1"):
    print("make a model with mecab tokenizer")
    mk_model("./out/token_mecab.txt", "./model/word2vec_mecab.model")
  else:
    print("make a model with ginza tokenizer")
    mk_model("./out/token_ginza.txt", "./model/word2vec_ginza.model")
  
  print("TIME(s):", time.perf_counter() - start)

  