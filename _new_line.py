"""
import re
import glob
files = glob.glob('./data/easy/*')

for file in files:
  with open(file, 'r') as r:
    content = r.read()
    content = content.replace("。\n","。")
    content = content.replace("。","。\n")
  
  with open(file, 'w') as w:
    w.write(content)
"""