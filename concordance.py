# Prompt4 KWIC上下文检索
from qhchina.analytics.collocations import kwic
import os

os.makedirs("output", exist_ok=True)
target_word = "君子"
sentence_files = ["lunyu_sentences.txt","zhouyi_sentences.txt"]

all_kwic_html = "<h1>KWIC 上下文检索：君子</h1>"
for sent_file in sentence_files:
    with open(sent_file,"r",encoding="utf-8") as f:
        # qhchina 要求分词后的词列表 list[list[str]]
        sentences = [line.strip().split() for line in f if line.strip()]
    kwic_result = kwic(sentences, target=target_word, horizon=10, separator=" ")
    all_kwic_html += f"<h2>{sent_file}</h2>"
    all_kwic_html += kwic_result.to_html()

with open("output/kwic.html","w",encoding="utf-8") as fw:
    fw.write(all_kwic_html)
print("KWIC上下文页面 output/kwic.html 完成")