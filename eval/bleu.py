import nltk
from nltk import word_tokenize
from nltk import bleu_score
import csv
import MeCab
tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

nltk.download('punkt')

def calc_bleu(text1, text2):
  hyp = word_tokenize(text1)
  ref = word_tokenize(text2)

  return round(bleu_score.sentence_bleu([ref], hyp), 4)

def calc_bleu_3gram(text1, text2):
  hyp = word_tokenize(text1)
  ref = word_tokenize(text2)

  return round(bleu_score.sentence_bleu([ref], hyp, (1./3., 1./3., 1./3.)), 4)


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
  with open('eval/T5/T5_75.csv', mode='r') as f:
    reader = csv.reader(f)
  
    eval = []
    for row in reader:
      x = calc_bleu_3gram(' '.join(mecab_tokenizer(row[0])), ' '.join(mecab_tokenizer(row[2])))
      eval.append(x)
      print(row[0])
      print(row[2])
      print(x)
    
    print("max = ", max(eval))
    print("average = ", sum(eval) / len(eval))


