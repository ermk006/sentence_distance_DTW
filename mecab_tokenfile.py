# コーパスを分かち書きしてword2veec学習用のテキストファイルを作る
import MeCab
import mojimoji as moji
import re
import preproc as pre
import time

start = time.perf_counter()
in_file = "data/corpus.txt"
out_file = "out/token_mecab.txt"

# コーパスの見込み
with open(in_file, encoding='UTF-8') as f:
  sentenses = [s.strip() for s in f.readlines()]

for line in sentenses:
  s = pre.mecab_tokenizer(pre.pre(line))
  s = '\n' + ' '.join(s)

  with open(out_file, 'a+', encoding='UTF-8') as wf:
    wf.write(s)

print("TIME(s):", time.perf_counter() - start)
