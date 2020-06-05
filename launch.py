import os

# os.mkdir('./tweet_result')
# os.mkdir('./tweet_per_day')
# os.mkdir('./tokenize_en_result')
# os.mkdir('./clean_en_tweet')
# os.mkdir('./bi_gram_folder')
# os.mkdir('./bi_images')
# os.mkdir('./tri_gram_folder')
# os.mkdir('./tri_images')

os.system("python ./tweets_process.py")
os.system("python ./tweet_ngram.py")
# os.system("python ./2.py")