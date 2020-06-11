#! /usr/bin/env python

import pandas as pd
import os
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
import tqdm

punctuation = list(string.punctuation)
stop_words = stopwords.words('italian') + punctuation

# print(stop_words)

def tweet_it_tokenizer(file):
    """
    对推特文本进行分词处理，并转为token list
    """
    tokenizer = TweetTokenizer()
    text = ''

    data = pd.read_csv(file, lineterminator='\n')
    es_data = data.loc[data.iloc[:,11] == 'es']
    for t in es_data.iloc[:,12]:
        text += t
    tokens = [i.lower() for i in tokenizer.tokenize(text)]

    return tokens

def clear_tokens(tokens):
    # 去除特殊语法和停用词
    tokens_c1 = [t for t in tokens if (len(t) >= 2)
                 and (not t.startswith(('#', '@')))
                 and (not t.startswith('http'))
                 and (t not in stop_words)
                 and (t[0].isalpha())]

    # ps = PorterStemmer()
    # stem_tokens = [ps.stem(w) for w in tokens_c1]

    return tokens_c1

def tokens_es_into_txts(file_path, output_path):
    # 负责把list数据写入各自的txt文件
    files = os.listdir(file_path)
    for file in tqdm.tqdm(files):
        if file[:-4] + '.txt' not in os.listdir(output_path):
            output_file = os.path.join(output_path, file[:-4] + '.txt')
            with open(output_file, 'w', encoding='UTF-8') as TargetFile:
                tokens = tweet_it_tokenizer(os.path.join(file_path, file))
                tokens_c1 = clear_tokens(tokens)

                output = ' '.join(tokens_c1)
                if tokens_c1 != []:
                    TargetFile.write(output)
                    print(output_file + '写入成功')
                    TargetFile.close()
                else:
                    print('当天没有这种语言的内容')
                    TargetFile.close()
                    os.remove(output_file)

if __name__ == '__main__':

    per_day_path = './tweet_per_day/2020-01'
    it_result_path = './tokenize_it_result'
    if it_result_path not in os.listdir():
        os.mkdir(it_result_path)

    print('____________clean token写入________________')
    tokens_es_into_txts(per_day_path, it_result_path)