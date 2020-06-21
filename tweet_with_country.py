#! /usr/bin/env python
import pandas as pd
import numpy as np
import math
import os



def get_country_code(per_day_dir, output_dir):

    files = os.listdir(per_day_dir)

    # df_ = pd.DataFrame(columns=['date', 'country_code', 'clean_text'])

    for file in files:
        row_list = []
        output_file = os.path.join(output_dir, file[:-4]+'.csv')
        file_path = os.path.join(per_day_dir, file)
        df = pd.read_csv(file_path, lineterminator='\n')
        df.columns = ['created_at', 'location', 'country_code', 'place_name', 'language', 'clean_text']
        for i in range(df.shape[0]):
            if str(df.loc[i, 'country_code']) != 'nan':
                dict1 = dict(date=df.iloc[i, 0], country_code=df.iloc[i, 2], place=df.iloc[i, 3],language = df.iloc[i,4], text=df.iloc[i, 5])
                row_list.append(dict1)
        df_ = pd.DataFrame(row_list)
        # print(df_)
        if row_list != []:
            df_.to_csv(output_file, encoding='utf-8', index=False)


if __name__ == '__main__':
    per_day_dir = './tweet_per_day/2020-01'
    output_dir = './tweet_with_loc'

    # os.mkdir(output_path)

    get_country_code(per_day_dir, output_dir)