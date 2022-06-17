import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

x = [[1, 2,3], [3,4,5],[1,1,5]]
y = [[2, 3,4], [4,5,6],[8,1,1]]

distance, path = fastdtw(x, y, dist=euclidean)


print("dist:", distance)
print("path:", path)
