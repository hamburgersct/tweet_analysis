#! /usr/bin/env python
from textblob import TextBlob
import pandas as pd
import os
import re
import tqdm
import numpy as np


def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

def sentiment_analysis(tweet_path, sentiment_file):
    # 将每天的tweet情感极性和主观性指数存储在sentiment_file中
    # NOTE: 请按照时间顺序执行，例如：先执行一月数据，再执行二月数据
    with open(sentiment_file, 'a', encoding='utf-8') as TargetFile:
        for file in tqdm.tqdm(sorted(os.listdir(tweet_path))):
            polarity, subjectivity = [], []
            df = pd.read_csv(os.path.join(tweet_path, file), lineterminator='\n')
            # TODO:这里的索引要改变
            for line in df.iloc[:,13]:
                polarity.append(get_tweet_sentiment(str(line))[0])
                subjectivity.append(get_tweet_sentiment(str(line))[1])
                # count += 1
            record = file[:-4] + "\t" + str(np.mean(polarity)) + "\t" + str(np.mean(subjectivity))
            TargetFile.write(record)
            TargetFile.write('\n')
        TargetFile.close()

if __name__ == '__main__':
    tweet_path = './tweet_per_day'
    sentiment_file = './polar_subject_file.txt'

    sentiment_analysis(tweet_path, sentiment_file)

