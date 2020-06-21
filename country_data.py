import pandas as pd
import os
import tqdm
'''
从所有有location tag的数据中提取特定国家和语言的数据
'''

def get_country_data(country_code, language, output_dir):
    # 提取指定国家、语言的数据存入csv文件夹
    file_path = 'F:/研究数据/loc_data'
    files = os.listdir(file_path)
    if output_dir not in os.listdir():
        os.mkdir(output_dir)

    df_list = []

    for file in tqdm.tqdm(files):
        df = pd.read_csv(os.path.join(file_path, file), encoding='utf-8')
        df_ = df.loc[df['country_code'] == country_code, :]
        df_lang = df_.loc[df['language'] == language, :]
        df_lang.to_csv(os.path.join(output_dir, file[:-4]), index=False)

def get_perday_text(csv_dir, txt_dir):
    # 提取csv中的文本数据到txt文件夹
    files = os.listdir(csv_dir)
    if txt_dir not in os.listdir():
        os.mkdir(txt_dir)

    for file in files:
        df = pd.read_csv(os.path.join(csv_dir, file), encoding='utf-8')
        text_list = df['text'].values
        with open(os.path.join(txt_dir, file+'.txt'), 'w', encoding='utf-8') as TargetFile:
            for text in text_list:
                TargetFile.write(str(text))
                TargetFile.write('\n')
            TargetFile.close()

if __name__ == '__main__':
    # get_country_data('MX', 'es', 'MX_es_data')
    # by_date('./country_data/US_data.csv')
    get_perday_text('./MX_es_data', 'MX_es_txt')
