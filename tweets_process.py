import re

import json_lines
import pandas as pd
import datetime as dt
import os
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string

id = []
created_at = []
text = []
clean_text = []
location = []
country_code = []
place_name = []
place_type = []
coordinates = []
favorite_count = []
retweet_count = []
verified = []
language = []
retweet = []

punctuation = list(string.punctuation)
stop_words = stopwords.words('english') + punctuation

columns = ['id', 'created_at', 'retweet', 'location', 'country_code', 'place_name', 'place_type', 'coordinates', 'favorite_count', 'retweet_count',
           'verified', 'language', 'text', 'clean_text']
df = pd.DataFrame(columns=columns)


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)|(#[A-Za-z0-9]+)", " ", tweet).split())

# Step1
def json_to_csv(file_path, output_path):
    """
    json格式文件转csv
    TODO:地理信息获取
    """

    files = os.listdir(file_path)
    for file in files:
        with open(os.path.join(file_path, file), 'r') as f:
            for item in json_lines.reader(f):

                id.append(item['id'])

                dateform = item['created_at'].split(' ')
                created_at.append(dateform[1] + ' ' + dateform[2])
                location.append(item['user']['location'])

                if item['place'] is None:
                    country_code.append(None)
                    place_name.append(None)
                    place_type.append(None)
                else:
                    country_code.append(item['place']['country_code'])
                    place_name.append(item['place']['name'])
                    place_type.append(item['place']['place_type'])

                if item['coordinates'] is None:
                    coordinates.append(item['coordinates'])
                else:
                    coordinates.append(item['coordinates']['coordinates'])

                favorite_count.append(item['favorite_count'])
                retweet_count.append(item['retweet_count'])
                verified.append(item['user']['verified'])
                language.append(item['lang'])

                full_text = item['full_text']
                if 'retweeted_status' in item:
                    retweet_stat = True
                    full_text = item['retweeted_status']['full_text']
                else:
                    retweet_stat = False
                if item['truncated'] == True:
                    full_text = item['extended_tweet']['full_text']
                clean_full = clean_tweet(full_text)
                text.append(full_text)
                clean_text.append(clean_full)

        # print(text)
        df['id'] = id
        df['created_at'] = created_at
        df['location'] = location
        df['country_code'] = country_code
        df['coordinates'] = coordinates
        df['favorite_count'] = favorite_count
        df['retweet_count'] = retweet_count
        df['verified'] = verified
        df['language'] = language
        df['text'] = text
        df['clean_text'] = clean_text
        df['retweet'] = retweet_stat
        df['place_type'] = place_type
        df['place_name'] = place_name

        # print(language)

        df.to_csv(os.path.join(output_path, file[-18:-5] + '.csv'), sep=',', index=False, encoding='UTF-8')
        df.drop(df.index, inplace=True)


# TODO:多语种分词器
def tweet_en_tokenizer(file):
    """
    对推特文本进行分词处理，并转为token list
    """
    tokenizer = TweetTokenizer()
    text = ''

    data = pd.read_csv(file)
    en_data = data.loc[data['language'] == 'en']
    for t in en_data['text']:
        text += t
    tokens = [i.lower() for i in tokenizer.tokenize(text)]

    return tokens


def clear_tokens(tokens):
    # 去除特殊语法和停用词
    tokens_c1 = [t for t in tokens if (len(t) >= 3)
                 and (not t.startswith(('#', '@')))
                 and (not t.startswith('http'))
                 and (t not in stop_words)
                 and (t[0].isalpha())]

    # ps = PorterStemmer()
    # stem_tokens = [ps.stem(w) for w in tokens_c1]

    return tokens_c1

# Step4
def tokens_en_into_txts(file_path, output_path):
    # 负责把list数据写入各自的txt文件
    files = os.listdir(file_path)
    for file in files:
        output_file = os.path.join(output_path, file[:-4] + '.txt')
        with open(output_file, 'w', encoding='UTF-8') as TargetFile:
            tokens = tweet_en_tokenizer(os.path.join(file_path, file))
            tokens_c1 = clear_tokens(tokens)
            # print('tokens length:' + str(len(tokens)))
            # print('tokens:' + str(tokens))
            # print('clear tokens length:' + str(len(tokens_c1)))

            output = ' '.join(tokens_c1)
            TargetFile.write(output)
            print(output_file + '写入成功')

# Step3
def cleaned_en_tweet(csv_file_path, output_path):
    # 把csv中clean_text写入文件，每条一行
    csv_files = os.listdir(csv_file_path)
    for file in csv_files:
        output_file = os.path.join(output_path, file[:-4] + '_clean_tw.txt')
        with open(output_file, 'w', encoding='UTF-8') as TargetFile:
            df = pd.read_csv(os.path.join(csv_file_path, file))
            tweet_list = list(df['clean_text'])
            for tweet in tweet_list:
                TargetFile.write(tweet)
                TargetFile.write('\n')
            print(os.path.join(output_path, file[:-4] + '_clean_tw.txt') + '写入成功')
            TargetFile.close()

# Step 2
def merge_per_day(csv_file_path, day_path):
    # 将每一天的csv文件汇总到一起
    files = os.listdir(csv_file_path)

    day_df = pd.DataFrame()
    df_list = []
    count = 0
    date = files[0][0:10]

    for file in files:
        date_name = file[:-7]
        count += 1
        if date_name == date:
            df = pd.read_csv(os.path.join(csv_file_path, file))
            print(file)
            df_list.append(df)
        else:
            # 先把原来的一天存好
            day_df = pd.concat(df_list)
            day_df.to_csv(os.path.join(day_path, date + '.csv'))
            print(f'{date}文件存入成功')
            # 更改date和df_list for a new day
            day_df.drop(day_df.index, inplace=True)
            date = date_name
            df_list.clear()
            df = pd.read_csv(os.path.join(csv_file_path, file))
            print(file)
            df_list.append(df)
    day_df = pd.concat(df_list)
    day_df.to_csv(os.path.join(day_path, date + '.csv'))
    print(f'{date}文件存入成功')

if __name__ == '__main__':
    file_path = './tweets'
    output_path = './tweet_result'
    per_day_path = './tweet_per_day'
    result_path = './tokenize_en_result'
    cleantw_path = './clean_en_tweet'

    print('____________json转csv________________')
    json_to_csv(file_path, output_path)

    # tokens = tweet_tokenizer('./tweet_result/tweets_examples.csv')
    # print(tokens)
    #
    # tokens_c1 = clear_tokens(tokens)
    # print(tokens_c1)
    # os.mkdir(result_path)
    print('\n')
    print('____________汇总每日csv________________')
    merge_per_day(output_path, per_day_path)

    print('\n')
    print('____________生成csv和txt________________')
    tokens_en_into_txts(per_day_path, result_path)

    print('\n')
    print('____________clean token写入________________')
    cleaned_en_tweet(per_day_path, cleantw_path)
