import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_path = './html/out/dtw_wmd.csv'

def main():
  csv_df = pd.read_csv(csv_path, header=None, names=['dtw', 'wmd'])
  csv_df = remove_all_zero_row(csv_df)


#  csv_df.colums[0] = csv_df.columns[0].apply(replace_log)
#  csv_df.colums[0] = np.log(csv_df.columns[0])

  data_x = csv_df[csv_df.columns[0]]
  data_x_log = np.log(csv_df[csv_df.columns[0]])
  data_y = csv_df[csv_df.columns[1]]

  csv_df.insert(1, 'dtw_log', data_x_log)
  print(csv_df)

  plt.figure(figsize=(10, 7))
  plt.xlabel("DTW")
  plt.ylabel("WMD")

  plt.scatter(data_x_log, data_y)
  plt.show()

  cor = csv_df.corr()
  print("相関係数" , cor)
  print(csv_df.describe())

def remove_all_zero_row(df):
    """全て0の行を削除"""
    df = df.copy()
    for row in df.index:
        if (df.loc[row] == 0).all():
            df.drop(row, axis=0, inplace=True)
    return df

def replace_log(n):
  return np.log(n)

if __name__=="__main__":
  main()
