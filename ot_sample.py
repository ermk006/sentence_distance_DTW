import numpy as np
import matplotlib as pl
import ot
import ot.plot


n = 100 # 各分布のサンプル数

#1つ目の分布パラメータ
mu_s = np.array([0, 0])
cov_s = np.array([[1, 0], [0, 1]])

#2つ目の分布パラメータ
mu_t = np.array([4, 4])
cov_t = np.array([[1, -.8], [-.8, 1]])

#2Dガウス分布で作成それぞれの分布を作成
xs = ot.datasets.make_2D_samples_gauss(n, mu_s, cov_s)
xt = ot.datasets.make_2D_samples_gauss(n, mu_t, cov_t)
#各点の重さ。今回は全て1/nとしている
a, b = np.ones((n,)) / n, np.ones((n,)) / n 

# 距離を定義する
# ot.distで、xsとxtの距離行列を計算する。
# https://pythonot.github.io/all.html?highlight=dist#ot.dist
M = ot.dist(xs, xt) 
M /= M.max()