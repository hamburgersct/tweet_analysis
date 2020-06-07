import os

if 'tweets' not in os.listdir():
    print('请先将所有tweet json文件放在./tweets目录下，然后再次运行')
    exit()

if 'tweet_result' not in os.listdir():
    os.mkdir('./tweet_result')
if 'tweet_per_day' not in os.listdir():
    os.mkdir('./tweet_per_day')
if 'tokenize_en_result' not in os.listdir():
    os.mkdir('./tokenize_en_result')
if 'clean_en_tweet' not in os.listdir():
    os.mkdir('./clean_en_tweet')
if 'bi_gram_folder' not in os.listdir():
    os.mkdir('./bi_gram_folder')
if 'bi_images' not in os.listdir():
    os.mkdir('./bi_images')
if 'tri_gram_folder' not in os.listdir():
    os.mkdir('./tri_gram_folder')
if 'tri_images' not in os.listdir():
    os.mkdir('./tri_images')

os.system("python ./tweets_process.py")
print('-----------------------')
print('------ngram分析--------')
print('-----------------------')
os.system("python ./tweet_ngram.py")
# os.system("python ./2.py")