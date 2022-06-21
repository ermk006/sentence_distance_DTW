import sen_to_vec as vec
#import pylab as plt
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

def plot(x, y, word_list=False):
  vec_x, word_x = vec.to_vector(x)
  vec_y, word_y = vec.to_vector(y)

  print("input1_len:",len(vec_x))
  print("input2_len:",len(vec_y))

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

if __name__=="__main__":
  easy = "お盆休みなどにお年寄りに会うときに気をつけることを、東北医科薬科大学の賀来満夫先生に聞きました。賀来先生は、ふるさとにお年寄りがいる場合は、帰るかどうかよく考えて決めてほしいと言っています。そして、ふるさとに帰る場合は、手をよく洗ってマスクをしっかりつけるようにします。"
  news = "お盆休みなどで高齢者と接する機会が増える際の注意点について、感染症の専門家は手洗いやマスクの着用などの基本的な対策に加え、一緒に過ごす時間を短くするなど、ポイントを絞って過ごし方を工夫してほしいとしています。お盆の帰省について感染症対策に詳しい東北医科薬科大学の賀来満夫特任教授は、帰省先に重症化のリスクが高い高齢者がいる場合は、帰省するかどうかは慎重に検討してほしいとしています。そのうえで、帰省した場合については、まずは基本的な感染対策として、こまめな手洗いや会話をする際にお互いに必ずマスクを着用するなどの対策を徹底することが必要だとしました。"
  plot(easy, news, word_list=True)
