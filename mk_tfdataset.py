from textwrap import indent
import pandas as pd
from sklearn.model_selection import train_test_split

in_file = "out/sentence_dist_dataset.csv"
train_news = "out/train_news.csv"
train_easy = "out/train_easy.csv"
val_news = "out/val_news.csv"
val_easy = "out/val_easy.csv"
test_news = "out/test_news.csv"
test_easy = "out/test_easy.csv"

border_dtw = 0.26
border_wmd = 0.63


df = pd.read_csv(in_file, header=None)

#df = df.sample(frac=1) #shuffle
df.columns = ['dtw', 'wmd', 'news', 'easy']

df_corpus = df[ (df['dtw'] <= border_dtw) & (df['wmd'] <= border_wmd) ]


df_train, df_test = train_test_split(df_corpus, test_size=0.1, random_state=0)

# test
df_test['news'].to_csv(test_news, header=False, index=False)
df_test['easy'].to_csv(test_easy, header=False, index=False)

df_train, df_val = train_test_split(df_train, test_size=0.1, random_state=0)

# train
df_train['news'].to_csv(train_news, header=False, index=False)
df_train['easy'].to_csv(train_easy, header=False, index=False)

# val
df_val['news'].to_csv(val_news, header=False, index=False)
df_val['easy'].to_csv(val_easy, header=False, index=False)

