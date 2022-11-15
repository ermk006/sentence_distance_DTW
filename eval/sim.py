import gensim
import numpy as np
import csv
import MeCab
tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

class w2v():
  def __init__(self):
    PATH = 'model/word2vec_mecab.model'
    #self.model = gensim.models.KeyedVectors.load_word2vec_format(PATH, binary=True)
    self.model = gensim.models.KeyedVectors.load_word2vec_format(PATH)

  def sentence_vec(self, words):
    vectors = []
    for w in words:
      if w in self.model.index_to_key:
        vectors.append(self.model[w])
    return vectors

  def phi(self, vec1, vec2):
    r = np.dot(vec1, vec2)/ (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return r


class similarity():
  def __init__(self) -> None:
    self.theta = 0.2 # 類似度0.5以上のみを単語アライメントに使用（梶原2018 平易なコーパスを用いないテキスト平易化）
    self.w2v = w2v()

  def average_alignment(self, sentence1, sentence2):
    li = []
    words1 = self.w2v.sentence_vec(sentence1)
    words2 = self.w2v.sentence_vec(sentence2)
    for w1 in words1:
      for w2 in words2:
        sim = self.w2v.phi(w1, w2)
        #print("w1:{} w2:{} sim:{}".format(w1, w2, sim))
        if sim >= self.theta:
          li.append(sim)
    return sum(li) / len(li) if li else 0

  def maximum_alignment(self, sentence1, sentence2):
    return self.s_max( self.s_asym(sentence1, sentence2), self.s_asym(sentence2, sentence1) )

  def calc_sim_hum(self, sentence1, sentence2):
    pass

  def s_asym(self, x, y):
    phi_max = 0
    li = []
    for xi in x:
      for yi in y:
        phi_max = max(self.w2v.phi(xi, yi), phi_max)
      li.append(phi_max)
    return sum(li) / len(li) if li else 0

  def s_max(self, x, y):
    return (x + y) / 2
    

def mecab_tokenizer(text):
  # テキストを分かち書きする関数を準備する
  parsed_lines = tagger.parse(text).split("\n")[:-2]
  surfaces = [l.split('\t')[0] for l in parsed_lines] # もとの形式
  features = [l.split('\t')[1] for l in parsed_lines] 
  # 原形を取得
  bases = [f.split(',')[6] for f in features]         # 原形
  # 配列で結果を返す
  token_list = [b if b != '*' else s for s, b in zip(surfaces, bases)]
  # アルファベットを小文字に統一
  token_list = [t.lower() for t in token_list]
  return token_list

if __name__=="__main__":
  sim = similarity()
  #text1 = "横断歩道の白線に茶褐色の影をつけると、横断歩道が浮いているように見えます"
  #text2 = "横断歩道の白線に茶褐色の影を付けるように塗装することで、ドライバーには近づくと浮かび上がって見え、注意を促すことが期待されるということです。"

  with open('eval/T5/T5_75.csv', mode='r') as f:
    reader = csv.reader(f)
  
    eval = []
    for row in reader:
      eval.append(sim.average_alignment(mecab_tokenizer(row[0]), mecab_tokenizer(row[2])))
    
    print(eval)
    print("average = ", sum(eval) / len(eval))

