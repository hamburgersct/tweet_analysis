import nltk
import os
from nltk.collocations import *
import plotly.graph_objects as go
import tqdm


def bi_grams(token_list):
    bgrams = nltk.bigrams(token_list)

    # compute frequency distribution for all the bigrams in the text
    fdist = nltk.FreqDist(bgrams)
    bigram_fq = fdist.most_common()
    bigram_freq_25 = {k: fdist.freq(k) for k, v in dict(bigram_fq[:10]).items()}

    # bigram_fq_25 = {k: v for k, v in dict(bigram_fq[:25]).items()}

    return bigram_freq_25


def tri_grams(token_list):
    trgrams = nltk.trigrams(token_list)

    fdist = nltk.FreqDist(trgrams)
    trigram_fq = fdist.most_common()
    trigram_fq_25 = {k: fdist.freq(k) for k, v in dict(trigram_fq[:10]).items()}

    return trigram_fq_25


def token_to_ngrams(file_path, bi_output_folder, tri_output_folder):
    # 将txt文件的分词结果转化为ngrams
    file_names = os.listdir(file_path)
    for file_name in file_names:
        # print(file_name)
        with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as f:
            bgram = {}
            trgram = {}
            # lines = f.readlines()

            for line in tqdm.tqdm(f):
                tokens = line.split()
                # print(bi_grams(tokens))
                bgram.update(bi_grams(tokens))
                print(len(tri_grams(tokens)))
                trgram.update(tri_grams(tokens))

        # 生成2gram词频图
        keys = [f'({key[0]},{key[1]})' for key in list(bgram.keys())]
        # print(len(keys))
        # print(len(list(bgram.values())))

        bi_fig = go.Figure(go.Bar(
            y=keys,
            x=list(bgram.values()),
            orientation='h',
        ))

        bi_fig.write_image(f"./bi_images/{file_name[:-4]}.svg")

        # 生成3gram词频图
        tri_keys = [f'({key[0]},{key[1]},{key[2]})' for key in list(trgram.keys())]

        tri_fig = go.Figure(go.Bar(
            y = tri_keys,
            x = list(trgram.values()),
            orientation='h',
        ))

        tri_fig.write_image(f"./tri_images/{file_name[:-4]}.svg")

        with open(os.path.join(bi_output_folder, file_name[:-4] + '.txt'), 'w') as bi_TargetFile:
            for k, v in bgram.items():
                # print(k, v)
                bi_TargetFile.write(f'({k[0]},{k[1]})' + ':' + str(v))
                bi_TargetFile.write('\n')
            bi_TargetFile.close()

        with open(os.path.join(tri_output_folder, file_name[:-4] + '.txt'), 'w') as tri_TargetFile:
            for k, v in trgram.items():
                tri_TargetFile.write(f'({k[0]},{k[1]},{k[2]})' + ':' + str(v))
                tri_TargetFile.write('\n')
            tri_TargetFile.close()


if __name__ == '__main__':

    file_path = './tokenize_en_result'
    bi_gram_folder = './bi_gram_folder'
    if 'bi_gram_folder' not in os.listdir():
        os.mkdir(bi_gram_folder)
    tri_gram_folder = './tri_gram_folder'
    if 'tri_gram_folder' not in os.listdir():
        os.mkdir(tri_gram_folder)

    token_to_ngrams(file_path, bi_gram_folder, tri_gram_folder)

    # print(bgram)
