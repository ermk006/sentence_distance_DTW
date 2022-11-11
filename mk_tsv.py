from textwrap import indent
import pandas as pd
from sklearn.model_selection import train_test_split

in_file = "out2/raw_sentence_dist_dataset.csv"
train_file = "out2/train.tsv"
dev_file = "out2/dev.tsv"
test_file = "out2/test.tsv"

# 類似度上位75%
#border_dtw = 0.90
#border_wmd = 0.90

# 類似度上位25%
border_dtw = 0.26
border_wmd = 0.63


df = pd.read_csv(in_file, header=None)

#df = df.sample(frac=1) #shuffle
df.columns = ['dtw', 'wmd', 'news', 'easy']

df_corpus = df[ (df['dtw'] <= border_dtw) & (df['wmd'] <= border_wmd) ]


df_temp, df_test = train_test_split(df_corpus, test_size=0.02, random_state=0)
df_train, df_dev = train_test_split(df_temp, test_size=0.05, random_state=0)

df_train = df_train.loc[:, ['easy', 'news']]
df_train['ID'] = 1
df_train.to_csv(train_file, sep='\t', header=False, index=False)

df_dev = df_dev.loc[:, ['easy', 'news']]
df_dev['ID'] = 1
df_dev.to_csv(dev_file, sep='\t', header=False, index=False)

df_test = df_test.loc[:, ['easy', 'news']]
df_test['ID'] = 1
df_test.to_csv(test_file, sep='\t', header=False, index=False)



