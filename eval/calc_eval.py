from bleu import mecab_tokenizer
from bleu import calc_bleu_3gram
from sim import similarity

import pandas as pd

in_file = 'eval/T5/T5_25.csv'


if __name__=="__main__":
  out_file = input("Output filename = ")
  sim = similarity()

  df = pd.read_csv(in_file, header=None, names=["out","ref","news"])
  eval_bleu = []
  eval_sim = []

  for row in df.values:
    x = calc_bleu_3gram(' '.join(mecab_tokenizer(row[0])), ' '.join(mecab_tokenizer(row[2])))
    eval_bleu.append(x)

    eval_sim.append(sim.average_alignment(mecab_tokenizer(row[0]), mecab_tokenizer(row[2])))

  df["bleu"] = eval_bleu
  df["sim"] = eval_sim

  df.to_csv(out_file)

  print("[BLEU]")
  print("max = ", max(eval_bleu))
  print("average = ", sum(eval_bleu) / len(eval_bleu))

  print("[VECTOR SIM]")
  print("max = ", max(eval_sim))
  print("average = ", sum(eval_sim) / len(eval_sim))
