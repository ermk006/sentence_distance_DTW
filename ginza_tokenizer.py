import spacy

nlp = spacy.load('ja_ginza')
 
def ginza_tokenizer(text):
  doc = nlp(text)
  token_list = []

  for token in doc:
    token_list.append(token.lemma_)

  token_list = [t.lower() for t in token_list]

  return token_list

if __name__=="__main__":
  s = "東京都では、新しいコロナウイルスの病気で亡くなった人が、７月までに３３３人いました。この中の３０６人は５月までに亡くなっていて、６月から７月は亡くなる人が減っています。亡くなった人の９３％は６０歳以上です。"
  print(ginza_tokenizer(s))