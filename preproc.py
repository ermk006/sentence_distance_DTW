import mojimoji as moji
import re
import MeCab
import spacy

nlp = spacy.load('ja_ginza')
tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

def pre(sentence):
  # 全角を半角へ（カタカナ除く）
  line = moji.zen_to_han(sentence, kana=False)
  # 全角記号を削除
  #line = re.sub("[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3001-\u303F]", '', line)
  line = re.sub("[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65]", '', line)
  # 半角記号を削除
  line = line.replace('"','')
  line = re.sub(r'[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~“”]', r' ', line)
  # 数字を0に変換, 桁区切りカンマは削除
  line = re.sub(r'(\d)([,.])(\d+)', r'\1\3', line)
  line = re.sub(r'\d+', '0', line)

  return line

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


def ginza_tokenizer(text):
  doc = nlp(text)
  token_list = []

  for token in doc:
    token_list.append(token.lemma_)

  token_list = [t.lower() for t in token_list]

  return token_list

def mecab_wakati(text):
  # テキストを分かち書きする関数を準備する
  parsed_lines = tagger.parse(text).split("\n")[:-2]
  surfaces = [l.split('\t')[0] for l in parsed_lines] # もとの形式
  return surfaces
