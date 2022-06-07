import MeCab
import mojimoji as moji
import re

in_file = "data/easy.txt"
out_file = "data/out_tokenizer.txt"
tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")


def mecab_tokenizer(text):
    # テキストを分かち書きする関数を準備する
    parsed_lines = tagger.parse(text).split("\n")[:-2]
    surfaces = [l.split('\t')[0] for l in parsed_lines]
    features = [l.split('\t')[1] for l in parsed_lines]
    # 原型を取得
    bases = [f.split(',')[6] for f in features]
    # 配列で結果を返す
    token_list = [b if b != '*' else s for s, b in zip(surfaces, bases)]
    # アルファベットを小文字に統一
    token_list = [t.lower() for t in token_list]
    return token_list


# コーパスの見込み
with open(in_file, encoding='UTF-8') as f:
  sentenses = [s.strip() for s in f.readlines()]

for line in sentenses:
  # 全角を半角へ（カタカナ除く）
  line = moji.zen_to_han(line, kana=False)
  # 全角記号を削除
  line = re.sub("[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]", '', line)

  s = mecab_tokenizer(line)
  s = ' '.join(s)
  with open(out_file, 'a', encoding='UTF-8') as wf:
    wf.write(s)
