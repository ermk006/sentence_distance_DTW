import nltk
from nltk import word_tokenize
from nltk import bleu_score
import MeCab

nltk.download('punkt')

def get_bleu(text1, text2):
  hyp = word_tokenize(text1)
  ref = word_tokenize(text2)

  return bleu_score.sentence_bleu([ref], hyp)


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
  print(get_bleu("子ども が ベランダ から 落ちる 事故 が 続く て いる ます 。","子ども の 転落事故 は 、 ことし に 入る て から も 相次ぐ で いる"))
