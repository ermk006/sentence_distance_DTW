import sen_to_vec as vec
#import pylab as plt
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

x = "気象庁と環境省は、東京都と千葉県、茨城県では７日に熱中症になる危険がとても高いと言って、「高温注意情報」を出しました。東京都と周りの８つの県では今年の７月から、高温注意情報の基準が新しくなりました。今までは気温だけで考えていましたが、湿度なども考えて出します。"
y = "東京都と千葉県、茨城県では7日、熱中症の危険性が極めて高くなると予想されています。気象庁と環境省は高温注意情報を発表し、熱中症に対する一層の対応を求めています。関東甲信ではことし7月から、高温注意情報の発表基準が予想最高気温から暑さ指数に変更されていますが、今回が初めての発表になります。"

vec_before = vec.to_vector(x)
vec_after = vec.to_vector(y)
print("input1_len:",len(vec_before))
print("input2_len:",len(vec_after))

distance, path = fastdtw(vec_before, vec_after, dist=euclidean)

#print(path)
y1 = [1 for i in range(len(vec_before))]
y2 = [0 for i in range(len(vec_after))]


import matplotlib.pyplot as plt
#plot signals
plt.plot(y1, label = 'Sequence 1')
plt.plot(y2, label = 'Sequence 2')
#plot alignment

for i, j in path:
    plt.plot((i, j), (y1[i], y2[j]), color = 'black')
plt.show()
