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
  #print(vec_x)

  #print("input1_len:",len(vec_x))
  #print("input2_len:",len(vec_y))

  if(rev==True):
    word_x.reverse()
    word_y.reverse()

  if(word_list==True):
    print("easy:",word_x)
    print("news:",word_y)


  return fastdtw(vec_x, vec_y, dist=euclidean)
  #print("distance:" ,distance)
  #print(path)
  #for xi, yi in path:
  #  print(word_x[xi], ":", word_y[yi])

def path_vec(x, y):
  return fastdtw(x, y, dist=euclidean)
  

if __name__=="__main__":
  easy = "気象庁と環境省は、東京都と千葉県、茨城県では７日に熱中症になる危険がとても高いと言って、「高温注意情報」を出しました。"
  news = "東京都と千葉県、茨城県では7日、熱中症の危険性が極めて高くなると予想されています。"

  path(easy, news, word_list=False, tokenizer="mecab")
  #graph(easy, news, word_list=False, tokenizer="mecab")
