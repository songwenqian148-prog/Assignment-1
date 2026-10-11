# Prompt2：搭配分析，3种参数运行，保存csv到output文件夹
from qhchina.analytics.collocations import find_collocates
from qhchina.helpers.texts import load_stopwords
import os
import pandas as pd

os.makedirs("output", exist_ok=True)
stopwords = load_stopwords("zh_cl_sim")
target_word = "君子"
sentence_files = ["lunyu_sentences.txt","zhouyi_sentences.txt"]

for sent_file in sentence_files:
    with open(sent_file,"r",encoding="utf-8") as f:
        # qhchina 要求分词后的词列表 list[list[str]]
        sentences = [line.strip().split() for line in f if line.strip()]
    # 三组参数
    runs = [
        ("window",5,f"{sent_file.replace('.txt','')}_window5.csv"),
        ("window",10,f"{sent_file.replace('.txt','')}_window10.csv"),
        ("sentence",None,f"{sent_file.replace('.txt','')}_sentence.csv")
    ]
    for method, horizon, out_csv in runs:
        df = find_collocates(
            sentences = sentences,
            target_words = target_word,
            method = method,
            horizon = horizon,
            filters = {
                "stopwords": stopwords,
                "min_obs_local": 2,
                "min_word_length": 2,
                "max_adjusted_p": 0.05
            },
            measures = ["log_likelihood","log_dice"],
            correction = "fdr_bh"
        )
        df = df.sort_values("log_dice", ascending=False)
        save_path = os.path.join("output",out_csv)
        df.to_csv(save_path, index=False, encoding="utf-8-sig")
        print(f"\n==== {out_csv} Top20 ====")
        print(df.head(20))