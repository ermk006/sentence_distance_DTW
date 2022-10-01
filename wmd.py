from gensim.models import word2vec
from gensim.models import KeyedVectors

path_model = "model/word2vec_mecab.model"

def main():
#    model = word2vec.Word2Vec.load(path_model)
    model = KeyedVectors.load_word2vec_format(path_model, binary=False)

    # 比較するテキストを分かち書き
    text_list1 = ["私","は","犬","が","好き","です"]
    text_list2 = ["私","は","猫","が","好き","です"]

    # word mover's distanceを実行
    sim_value = model.wmdistance(text_list1, text_list2)

    print(text_list1)
    print(text_list2)
    print(sim_value)

# text_list1, text_list2 は分かち書き済みの単語リスト
def wmd_distance(text_list1, text_list2):
    model = KeyedVectors.load_word2vec_format(path_model, binary=False)

    # word mover's distanceを実行
    sim_value = model.wmdistance(text_list1, text_list2)
    return sim_value

if __name__=="__main__":
  main()
