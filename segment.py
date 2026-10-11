# Prompt1：分句、繁转简、jieba分词
import jieba
import opencc
import csv

# 配置
converter = opencc.OpenCC('t2s.json')
userdict_path = "userdict.txt"
jieba.load_userdict(userdict_path)
target_files = ["lunyu.txt", "zhouyi.txt"]
end_punc = {"。", "！", "？", "；"}

for filename in target_files:
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read()
    # 繁体转简体
    simp_text = converter.convert(raw)
    # 分句
    sentences = []
    current_sent = []
    for char in simp_text:
        current_sent.append(char)
        if char in end_punc:
            sent = "".join(current_sent).strip()
            if len(sent)>=5:
                sentences.append(sent)
            current_sent = []
    # jieba分词，去除标点
    seg_result = []
    for sent in sentences:
        words = jieba.lcut(sent)
        words_clean = [w for w in words if len(w.strip())>1 or w=="君子"]
        seg_result.append(" ".join(words_clean))
    # 保存 sentences.txt
    out_name = filename.replace(".txt","_sentences.txt")
    with open(out_name,"w",encoding="utf-8") as fw:
        fw.write("\n".join(seg_result))
    print(f"{filename} 分词完成，输出 {out_name}")
    # 隐随机打印20条包含「君子」的句子，人工校验分词
    import random
    sample = [s for s in seg_result if "君子" in s]
    print(f"\n===== 抽样20条含君子的句子 {filename} =====")
    print(random.sample(sample, min(20,len(sample))))