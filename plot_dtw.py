import sen_to_vec as vec
#import pylab as plt
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

def graph(x, y, word_list=False, rev=False, tokenizer="mecab"):
  vec_x, word_x = vec.to_vector(x, tokenizer)
  vec_y, word_y = vec.to_vector(y, tokenizer)

  print("input1_len:",len(vec_x))
  print("input2_len:",len(vec_y))

  if(rev==True):
    word_x.reverse()
    word_y.reverse()

  if(word_list==True):
    print("easy:",word_x)
    print("news:",word_y)

  distance, path = fastdtw(vec_x, vec_y, dist=euclidean)
  print("distance:" ,distance)

  #print(path)
  y1 = [1 for i in range(len(vec_x))]
  y2 = [0 for i in range(len(vec_y))]

  import matplotlib.pyplot as plt
  #plot signals
  plt.plot(y1)
  plt.plot(y2)
  #plot alignment

  for i, j in path:
      plt.plot((i, j), (y1[i], y2[j]), color = 'black')
  plt.show()
  

def path(x, y, word_list=False, rev=False, tokenizer="mecab"):
  vec_x, word_x = vec.to_vector(x, tokenizer)
  vec_y, word_y = vec.to_vector(y, tokenizer)

  print("input1_len:",len(vec_x))
  print("input2_len:",len(vec_y))

  if(rev==True):
    word_x.reverse()
    word_y.reverse()

  if(word_list==True):
    print("easy:",word_x)
    print("news:",word_y)

  distance, path = fastdtw(vec_x, vec_y, dist=euclidean)
  print("distance:" ,distance)
  print(path)
  for xi, yi in path:
    print(word_x[xi], ":", word_y[yi])
  

if __name__=="__main__":
#  easy = "お盆休みなどにお年寄りに会うときに気をつけることを、東北医科薬科大学の賀来満夫先生に聞きました。賀来先生は、ふるさとにお年寄りがいる場合は、帰るかどうかよく考えて決めてほしいと言っています。そして、ふるさとに帰る場合は、手をよく洗ってマスクをしっかりつけるようにします。"
#  news = "お盆休みなどで高齢者と接する機会が増える際の注意点について、感染症の専門家は手洗いやマスクの着用などの基本的な対策に加え、一緒に過ごす時間を短くするなど、ポイントを絞って過ごし方を工夫してほしいとしています。お盆の帰省について感染症対策に詳しい東北医科薬科大学の賀来満夫特任教授は、帰省先に重症化のリスクが高い高齢者がいる場合は、帰省するかどうかは慎重に検討してほしいとしています。そのうえで、帰省した場合については、まずは基本的な感染対策として、こまめな手洗いや会話をする際にお互いに必ずマスクを着用するなどの対策を徹底することが必要だとしました。"
  file_easy = "./data/easy/001.txt"
  file_news = "./data/news/001.txt"
  #easy = "東京都では、新しいコロナウイルスの病気で亡くなった人が、７月までに３３３人いました。この中の３０６人は５月までに亡くなっていて、６月から７月は亡くなる人が減っています。亡くなった人の９３％は６０歳以上です。"
  #news = "新型コロナウイルスは先月、全国で一気に感染が広がりました。中でも、全国で最も感染確認が多い東京都の状況を見てみると、緊急事態宣言が出された4月と比べて特に状況が変化しています。新規陽性者数 新型コロナウイルスの「新規陽性者数」を月別で見ると▽これまで最も多かった、4月の3748人に対し▽7月は6466人となり、およそ1.7倍に増加しました。"

  path(easy, news, word_list=False, tokenizer="mecab")
  #graph(easy, news, word_list=False, tokenizer="mecab")
